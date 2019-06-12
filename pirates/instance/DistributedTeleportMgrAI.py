from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from otp.ai.MagicWordGlobal import *

from pirates.quest.QuestConstants import LocationIds
from pirates.piratesbase import PiratesGlobals
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.instance.DistributedTeleportZoneAI import DistributedTeleportZoneAI
from pirates.instance.DistributedTeleportHandlerAI import DistributedTeleportHandlerAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI


class TeleportOperationFSM(FSM):

    def __init__(self, air, avatar, world, gameArea, spawnPt):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.avatar = avatar
        self.world = world
        self.gameArea = gameArea
        self.spawnPt = spawnPt

        self.teleportZone = None
        self.teleportHandler = None

        # just incase the avatar disconnects before we can complete the teleport
        # process, handle cleanup appropriately...
        self.acceptOnce(self.avatar.getDeleteEvent(), self.cleanup)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def cleanup(self):
        del self.air.teleportMgr.avatar2fsm[self.avatar.doId]
        self.ignoreAll()
        self.demand('Off')

class TeleportFSM(TeleportOperationFSM):

    def __teleportZoneArrivedCallback(self, teleportZone):
        if not teleportZone:
            self.notify.warning('Failed to generate the teleport zone for avatar %d, '
                'while trying to teleport!' % self.avatar.doId)

            self.cleanup()
            return

        teleportHandlerDoId = self.air.allocateChannel()
        self.acceptOnce('generate-%d' % teleportHandlerDoId,
            self.__teleportHandlerArrivedCallback)

        self.teleportHandler = DistributedTeleportHandlerAI(self.air,
            self.air.teleportMgr, self, self.avatar)

        self.teleportHandler.generateWithRequiredAndId(teleportHandlerDoId,
            self.air.districtId, self.teleportZone.zoneId)

    def __teleportHandlerArrivedCallback(self, teleportHandler):
        if not teleportHandler:
            self.notify.warning('Failed to generate the teleport handler for avatar %d, '
                'while trying to teleport!' % self.avatar.doId)

            self.cleanup()
            return

        self.avatar.d_forceTeleportStart(self.world.getFileName(), self.teleportZone.doId,
            self.teleportHandler.doId, 0, self.teleportZone.parentId, self.teleportZone.zoneId)

    def enterTeleporting(self):
        teleportZoneDoId = self.air.allocateChannel()
        self.acceptOnce('generate-%d' % teleportZoneDoId,
            self.__teleportZoneArrivedCallback)

        self.teleportZone = DistributedTeleportZoneAI(self.air)
        self.teleportZone.generateWithRequiredAndId(teleportZoneDoId,
            self.air.districtId, self.air.allocateZone())

    def exitTeleporting(self):
        if self.teleportZone:
            self.teleportZone.requestDelete()
            self.teleportZone = None

        if self.teleportHandler:
            self.teleportHandler.requestDelete()
            self.teleportHandler = None


class DistributedTeleportMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatar2fsm = {}

    def getWorld(self, instanceType, instanceName):
        for object in self.air.doId2do.values():
            if not object or not isinstance(object, DistributedInstanceBaseAI):
                continue

            if object.getType() == instanceType and object.getFileName() == instanceName:
                return object

        return None

    def d_initiateTeleport(self, avatar, instanceType=None, instanceName=None, locationUid=None, spawnPt=None):
        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot initiate teleport for avatar %d, '
                'already teleporting!' % avatar.doId)

            return

        returnLocation = avatar.getReturnLocation()
        currentIsland = avatar.getCurrentIsland()

        # check to see which island the avatar exited last at,
        # then ensure this is their login teleport; not a normal teleport request...
        if returnLocation and not currentIsland:
            locationUid = returnLocation

        gameArea = avatar.getParentObj()
        if isinstance(gameArea, DistributedGameAreaAI) and gameArea.getUniqueId() == locationUid:
            self.notify.warning('Cannot initiate teleport for %d, '
                'already there, locationUid=%s!' % (avatar.doId, locationUid))

            return

        if not instanceType and not instanceName:
            world = gameArea.getParentObj()
        else:
            world = self.getWorld(instanceType, instanceName)

        if not world or not isinstance(world, DistributedInstanceBaseAI):
            self.notify.warning('Cannot initiate teleport for unknown world: '
                'instanceType=%r instanceName=%r' % (instanceType, instanceName))

            return

        gameArea = self.air.uidMgr.justGetMeMeObject(locationUid)
        if not gameArea:
            self.notify.warning('Cannot initiate teleport for unknown '
                'gameArea: locationUid=%r' % locationUid)

            return

        if not spawnPt:
            # TODO FIXME!
            # if we have no spawn point for this world and we need to retrieve one,
            # then let's assume the world is the game area's parent... When teleporting
            # from an interior to an exterior, the world is not the game area's parent...?
            world = gameArea.getParentObj()
            spawnPt = world.getSpawnPt(gameArea.getUniqueId())

        if not spawnPt:
            self.notify.warning('Cannot initiate teleport for avatar %d, no available spawn points '
                'for gameArea, locationUid=%r!' % (avatar.doId, locationUid))

            return

        self.avatar2fsm[avatar.doId] = TeleportFSM(self.air,
            avatar, world, gameArea, spawnPt)

        self.avatar2fsm[avatar.doId].request('Teleporting')

    def initiateTeleport(self, instanceType, fromInstanceType, shardId, locationUid, instanceDoId, instanceName, gameType, friendDoId, friendAreaDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if shardId and shardId != self.air.districtId:
            self.air.travelAgent.d_requestTeleportToShardAItoUD(avatar.doId, shardId, instanceType,
                instanceName, locationUid)

            return

        self.d_initiateTeleport(avatar, instanceType, instanceName, locationUid)

    def requestTeleportToIsland(self, locationUid):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        self.d_initiateTeleport(avatar, locationUid=locationUid)

    def d_teleportHasBegun(self, avatarId, instanceType, fromInstanceType, instanceName, gameType):
        self.sendUpdateToAvatarId(avatarId, 'teleportHasBegun', [instanceType, fromInstanceType,
            instanceName, gameType])

    def d_localTeleportToIdResponse(self, avatarId, parentId, zoneId):
        self.sendUpdateToAvatarId(avatarId, '_localTeleportToIdResponse', [parentId, zoneId])


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def areaTeleport(locationUid):
    if locationUid == 'portroyal':
        locationUid = '1150922126.8dzlu'
    elif locationUid == 'tortuga':
        locationUid = '1156207188.95dzlu'
    elif locationUid == 'delfuego':
        locationUid = '1142018473.22dxschafe'
    elif locationUid == 'tormenta':
        locationUid = '1164150392.42dzlu'
    elif locationUid == 'devilsanvil':
        locationUid = '1164135492.81dzlu'
    elif locationUid == 'outcast':
        locationUid = '1173381952.2sdnaik'

    avatar = spellbook.getTarget()
    simbase.air.teleportMgr.d_initiateTeleport(avatar, locationUid=locationUid)
    return 'Teleporting avatar %d to area: %s...' % (avatar.doId, areaUid)
