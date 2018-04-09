from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory

class DistributedInventoryManagerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

        self.inventories = {}
        self.inventoryTasks = {}

    def hasInventory(self, inventoryId):
        return inventoryId in self.inventories

    def addInventory(self, inventory):
        if self.hasInventory(inventory.doId):
            self.notify.debug('Tried to add an already existing inventory %d!' % inventory.doId)
            return

        self.inventories[inventory.doId] = inventory

    def removeInventory(self, inventory):
        if not self.hasInventory(inventory.doId):
            self.notify.debug('Tried to remove a non-existant inventory %d!' % inventory.doId)
            return

        del self.inventories[inventory.doId]
        inventory.requestDelete()

    def getInventory(self, avatarId):
        for inventory in self.inventories.values():

            if inventory.getOwnerId() == avatarId:
                return inventory

        return None

    def requestInventory(self):
        avatarId = self.air.getAvatarIdFromSender()

        if not avatarId:
            return

        def queryResponse(dclass, fields):
            if not dclass or not fields:
                self.notify.debug('Failed to query avatar %d!' % avatarId)
                return

            inventoryId, = fields.get('setInventoryId', (0,))

            if not inventoryId:
                self.notify.debug('Invalid inventory found for avatar %d!' % avatarId)
                return

            self.__sendInventory(avatarId, inventoryId)

        self.air.dbInterface.queryObject(self.air.dbId, avatarId, callback=queryResponse, dclass=\
            self.air.dclassesByName['DistributedPlayerPirateAI'])

    def __waitForInventory(self, avatarId, inventoryId, task):
        inventory = self.inventories.get(inventoryId)

        if not inventory:
            return task.again

        self.__sendInventory(avatarId, inventory.doId)
        return task.done

    def __cleanupWaitForInventory(self, avatarId):
        if avatarId not in self.inventoryTasks:
            return

        taskMgr.remove(self.inventoryTasks[avatarId])
        del self.inventoryTasks[avatarId]

    def __sendInventory(self, avatarId, inventoryId):
        inventory = self.inventories.get(inventoryId)

        self.acceptOnce('distObjDelete-%d' % (avatarId), lambda: \
            self.__cleanupWaitForInventory(avatarId))

        if not inventory:
            if avatarId in self.inventoryTasks:
                self.notify.debug('Cannot retrieve inventory for avatar %d, already trying to get inventory!' % (
                    avatarId))

                return

            self.inventoryTasks[avatarId] = taskMgr.doMethodLater(1.0, self.__waitForInventory, 'waitForInventory-%d-%s' % (
                avatarId, id(self)), appendTask=True, extraArgs=[avatarId, inventoryId])

            return

        avatar = self.air.doId2do.get(avatarId)

        if not avatar:
            self.notify.debug('Cannot send inventory, unknown avatar!')
            return

        inventory.b_setStackLimit(InventoryType.Hp, avatar.getMaxHp())
        inventory.b_setStackLimit(InventoryType.Mojo, avatar.getMaxMojo())

        def inventoryResponse(dclass, fields):
            if not dclass or not fields:
                self.notify.debug('Failed to query inventory %d!' % avatarId)
                return

            accumulators, = fields.get('setAccumulators', [])
            stackLimits, = fields.get('setStackLimits', [])
            stacks, = fields.get('setStacks', [])

            for accumulator in accumulators:
                inventory.b_setAccumulator(*accumulator)

            inventory.b_setStackLimits(stackLimits)

            for stack in stacks:
                inventory.b_setStack(*stack)

            inventory.d_requestInventoryComplete()

        self.air.dbInterface.queryObject(self.air.dbId, inventoryId, callback=inventoryResponse, dclass=\
            self.air.dclassesByName['DistributedInventoryAI'])
