from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM

from otp.distributed.OtpDoGlobals import *
from otp.ai.MagicWordGlobal import *

from pirates.quest.DistributedQuestAI import DistributedQuestAI
from pirates.quest.QuestTaskState import QuestTaskState
from pirates.quest.QuestRewardStruct import QuestRewardStruct
from pirates.quest import QuestEvent
from pirates.quest import QuestDB
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.uberdog.UberDogGlobals import InventoryCategory


class QuestOperationFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestOperationFSM')

    def __init__(self, air, avatar):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.avatar = avatar

    def enterOff(self):
        pass

    def exitOff(Self):
        pass

class CreateQuestFSM(QuestOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('CreateQuestFSM')

    def enterCreate(self, questId):
        self.inventory = self.avatar.getInventory()
        if not self.inventory:
            self.notify.warning('Failed to create quest %s for avatar %d, '
                'no inventory found!' % (questId, self.avatar.doId))

            self.cleanup()
            return

        fields = {
            'setQuestId': (questId,),
            'setGiverId': ('',),
            'setCombineOp': (0,),
            'setTaskStates': ([QuestTaskState()],),
            'setRewardStructs': ([],),
        }

        def questCreatedCallback(questDoId):
            if not questDoId:
                self.notify.warning('Failed to create quest %s for avatar %d!' % (
                    questId, self.avatar.doId))

                self.cleanup()
                return

            def questActivatedCallback(quest):
                if not quest:
                    self.notify.warning('Failed to activate quest %d for avatar %d, '
                        'quest failed to generate!' % (questDoId, self.avatar.doId))

                    self.cleanup()
                    return

                # update the avatar's quest list so the quest will be stored in
                # the database so we can retrieve and activate it later...
                questList = self.inventory.getDoIdListCategory(InventoryCategory.QUESTS)
                questList.append(questDoId)
                self.inventory.setQuestList(questList)

                # we're done.
                self.cleanup()

            self.air.questMgr.activateQuest(self.avatar, questDoId,
                questActivatedCallback)

        self.air.dbInterface.createObject(self.air.dbId,
            self.air.dclassesByName['DistributedQuestAI'],
            fields,
            questCreatedCallback)

    def exitCreate(self):
        pass

class ActivateQuestsFSM(QuestOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('ActivateQuestsFSM')

    def enterActivate(self):
        self.inventory = self.avatar.getInventory()
        if not self.inventory:
            self.notify.warning('Failed to activate quests for avatar %d, '
                'no inventory found!' % (questId, self.avatar.doId))

            self.cleanup()
            return

        self.questList = self.inventory.getDoIdListCategory(InventoryCategory.QUESTS)
        for questDoId in self.questList:
            # check to see if the quest object has already been generated,
            # we do not want to regenerate the object over again...
            if questDoId in self.air.doId2do:
                continue

            def queryQuestCallback(dclass, fields, questDoId=questDoId):
                if not dclass and not fields:
                    self.notify.warning('Failed to query quest %d, quest not found!' % (
                        questDoId))

                    self.cleanup()
                    return

                def questActivatedCallback(quest):
                    if not quest:
                        self.notify.warning('Failed to activate quest %d for avatar %d, '
                            'quest failed to generate!' % (questDoId, self.avatar.doId))

                        self.cleanup()
                        return

                    self.questList.remove(questDoId)
                    if not self.questList:
                        self.cleanup()

                self.air.questMgr.activateQuest(self.avatar, questDoId,
                    questActivatedCallback)

            self.air.dbInterface.queryObject(self.air.dbId,
                questDoId,
                queryQuestCallback,
                self.air.dclassesByName['DistributedQuestAI'])

    def exitActivate(self):
        pass

class QuestManagerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestManagerAI')

    def __init__(self, air):
        self.air = air
        self.quests = {}

    def hasQuest(self, avatar, questDoId=None, questId=None):
        return self.getQuest(avatar, questDoId, questId) is not None

    def createQuest(self, avatar, questId):
        fsm = CreateQuestFSM(self.air, avatar)
        fsm.request('Create', questId)

    def activateQuest(self, avatar, questDoId, callback):
        activeQuests = self.quests.setdefault(avatar.doId, {})
        if questDoId in activeQuests:
            self.notify.warning('Cannot add a new quest %d for avatar %d, '
                'quest already added!' % (questDoId, avatar.doId))

            return

        def questArrivedCallback(quest):
            if not quest:
                self.notify.warning('Failed to activate quest %d for avatar %d!' % (
                    questDoId, avatar.doId))

                # call the callback and let them know the quest failed
                # to activate on the dbss...
                callback(None)
                return

            # set the owner of the quest object, this will then send an
            # OwnerView object generate to the client...
            channel = avatar.getDISLid() << 32 | avatar.doId
            self.air.setOwner(quest.doId, channel)

            # store the new quest object to the dictionary of quest objects
            # so we can keep track of it for later use...
            self.quests[avatar.doId][quest.doId] = quest

            # finally, call the callback specified and let them know,
            # the quest has been activated...
            callback(quest)

        self.acceptOnce('generate-%d' % questDoId, questArrivedCallback)
        self.air.sendActivate(questDoId, self.air.districtId, OTP_ZONE_ID_MANAGEMENT,
            self.air.dclassesByName['DistributedQuestAI'])

    def activateQuests(self, avatar):
        fsm = ActivateQuestsFSM(self.air, avatar)
        fsm.request('Activate')

    def deactivateQuest(self, avatar, questDoId):
        if not self.hasQuest(avatar, questDoId):
            self.notify.warning('Cannot drop deactivate %d for avatar %d, '
                'quest never added!' % (questDoId, avatar.doId))

            return

        quest = self.quests[avatar.doId].pop(questDoId)
        quest.requestDelete()
        del quest

    def deactivateQuests(self, avatar):
        if avatar.doId not in self.quests:
            return

        for questDoId in list(self.quests[avatar.doId]):
            self.deactivateQuest(avatar, questDoId)

    def dropQuest(self, avatar, quest):
        if not self.hasQuest(avatar, quest.doId):
            self.notify.warning('Cannot drop quest %d for avatar %d, '
                'quest never added!' % (quest.doId, avatar.doId))

            return

        inventory = avatar.getInventory()
        if not inventory:
            self.notify.debug('Failed to drop quest %d for avatar %d, '
                'no inventory found!' % (quest.doId, avatar.doId))

            return

        questList = inventory.getDoIdListCategory(InventoryCategory.QUESTS)
        if quest.doId not in questList:
            self.notify.warning('Cannot drop quest %d for avatar %d, '
                'quest not found!' % (quest.doId, avatar.doId))

            return

        # update the player's quest list on their inventory...
        questList.remove(quest.doId)
        inventory.setQuestList(questList)

        # update the player's quest history so that we will not ever give
        # the player the same quest again...
        questHistory = avatar.getQuestHistory()
        questHistory.append(quest.questDNA.getQuestInt())
        avatar.b_setQuestHistory(questHistory)

        # finally, deactivate the old quest.
        self.deactivateQuest(avatar, quest.doId)
        messenger.send(quest.getDroppedEventString())

    def dropQuests(self, avatar):
        if avatar.doId not in self.quests:
            return

        for quest in list(self.quests[avatar.doId].values()):
            self.dropQuest(avatar, quest)

    def getQuest(self, avatar, questDoId=None, questId=None):
        if not questDoId and not questId:
            return None

        if avatar.doId not in self.quests:
            return None

        questList = self.quests[avatar.doId]
        if questId is not None:
            for quest in list(questList.values()):
                if quest.questId == questId:
                    return quest

        return questList.get(questDoId)

    def completeQuest(self, avatar, quest):
        questInt = quest.questDNA.getQuestInt()
        self.dropQuest(avatar, quest)

        try:
            nextQuestId = QuestDB.getQuestIdFromQuestInt(questInt + 1)
        except KeyError:
            return

        self.createQuest(avatar, nextQuestId)

    def __completeTaskState(self, avatar, questEvent, callback=None):
        activeQuest = self.getQuest(avatar, questId=avatar.getActiveQuest())
        if not activeQuest:
            return

        taskDNAs = activeQuest.questDNA.getTaskDNAs()
        taskStates = activeQuest.getTaskStates()

        # iterate through all of the task states and check to see if we
        # have successfully completed one...
        for x in xrange(len(taskStates)):
            taskDNA = taskDNAs[x]
            taskState = taskStates[x]

            # check to see if the task state event has been completed.
            if questEvent.applyTo(taskState, taskDNA):
                taskDNA.complete(questEvent, taskState)
                if taskState.isComplete():
                    if callback is not None:
                        callback()
                    else:
                        self.completeQuest(avatar, activeQuest)

                break

    def enemyDefeated(self, avatar, enemy):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        questEvent = QuestEvent.EnemyDefeated()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setEnemyType(enemy.getAvatarType())
        questEvent.setLevel(enemy.getLevel())
        questEvent.setWeaponType(enemy.getCurrentWeapon()[0])

        self.__completeTaskState(avatar, questEvent)

    def requestInteract(self, avatar, npc):
        activeQuest = self.getQuest(avatar, questId=avatar.getActiveQuest())
        if not activeQuest:
            return

        if isinstance(npc, DistributedNPCTownfolkAI):
            questEvent = QuestEvent.NPCVisited()
            questEvent.setNpcId(npc.getUniqueId())
            questEvent.setAvId(avatar.doId)
        else:
            self.notify.warning('Avatar %d failed to request interact for npc %d, '
                'invalid npc type!' % (avatar.doId, npc.doId))

            return

        def interactCallback():

            def questFinalizeCallback():
                self.completeQuest(avatar, activeQuest)

            self.accept('quest-finalize-%d' % activeQuest.doId, questFinalizeCallback)
            activeQuest.d_startFinalizeScene(0, 0)

        self.__completeTaskState(avatar, questEvent, callback=interactCallback)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def addQuest(questId):
    invoker = spellbook.getInvoker()
    if simbase.air.questMgr.hasQuest(invoker, questId=questId):
        return 'Avatar already has active quest: %s!' % questId

    simbase.air.questMgr.createQuest(invoker, questId)
    return 'Added new active quest: %s.' % questId

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def dropQuest(questId):
    invoker = spellbook.getInvoker()
    activeQuest = simbase.air.questMgr.getQuest(invoker, questId=questId)
    if not activeQuest:
        return 'Could not find active quest: %s' % questId

    simbase.air.questMgr.dropQuest(invoker, activeQuest.doId)
    return 'Dropped active quest: %s!' % questId

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def dropAllQuests():
    simbase.air.questMgr.dropQuests(spellbook.getInvoker())
    return 'Dropped all active quests.'
