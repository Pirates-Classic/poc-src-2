from pirates.world.WorldCreatorBase import WorldCreatorBase
from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import ObjectList
from pirates.instance.DistributedMainWorldAI import DistributedMainWorldAI

class WorldCreatorAI(WorldCreatorBase, DirectObject):
    notify = directNotify.newCategory('WorldCreatorAI')

    def __init__(self, air):
        self.air = air
        self.world = None

        WorldCreatorBase.__init__(self, air)

    @classmethod
    def isObjectInCurrentGamePhase(cls, object):
        return True

    def loadObjectsFromFile(self, filename, parent=None, zoneLevel=0, startTime=None, parentIsObj=False):
        return WorldCreatorBase.loadObjectsFromFile(self, filename, parent, zoneLevel, startTime, parentIsObj)

    def getObjectParentUid(self, objKey):
        found = None
        for fileName in self.fileDicts.keys():
            found = self.getObjectDataFromFileByUid(objKey, fileName)
            if found:
                break

        return found

    def getObjectFilenameByUid(self, objKey, getParentUid=True):
        file = None
        for fileName in self.fileDicts.keys():
            found = self.getObjectDataFromFileByUid(objKey, fileName)
            if found:
                file = fileName
                break

        return file

    def createObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel=0, startTime=None, parentIsObj=False, fileName=None, actualParentObj=None):
        objType = WorldCreatorBase.createObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel, startTime, parentIsObj, fileName, actualParentObj)

        if not objType:
            return (None, None)

        newObj = None
        objParent = None

        if objType == ObjectList.AREA_TYPE_WORLD_REGION:
            objParent = self.__createWorldInstance(object, parent, parentUid, objKey, dynamic)
        else:
            newObj = self.world.builder.createObject(objType, object, parent, parentUid, objKey, dynamic, parentIsObj, fileName, actualParentObj)

        return (newObj, objParent)

    def __createWorldInstance(self, objectData, parent, parentUid, objKey, dynamic):
        self.world = DistributedMainWorldAI(self.air)
        self.world.setUniqueId(objKey)
        self.world.setName(objectData.get('Name', 'default'))
        self.world.generateWithRequired(PiratesGlobals.InstanceUberZone)

        self.air.uidMgr.addUid(self.world.getUniqueId(), self.world.doId)
        return self.world
