from direct.showbase.PythonUtil import StackTrace, report
from pirates.piratesgui.RadarGui import *
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode


class QuestIndicatorNodeQuestNode(QuestIndicatorNode):

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'QuestNodeIndicator', [50], questStep)
        return

    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        self.ignore('tunnelSetLinks')
        QuestIndicatorNode.delete(self)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def placeInWorld(self):
        originObj = base.cr.doId2do.get(self.questStep.getOriginDoId())
        if originObj:
            posH = self.questStep.getPosH()
            pos, h = posH[:3], posH[3]
            self.reparentTo(originObj)
            self.setPos(*pos)
            self.setHpr(h, 0, 0)

    def loadZoneLevel(self, level):
        if level == 0:
            self.request('At')
        else:
            if level == 1:
                self.request('Far')

    def unloadZoneLevel(self, level, cacheObs=False):
        if level == 0:
            self.request('Far')
        else:
            if level == 1:
                self.request('Off')

    def enterFar(self):
        QuestIndicatorNode.enterFar(self)
        self.farEffect.setEffectScale(1.5)

    def exitFar(self):
        self.farEffect.setEffectScale(1)
        QuestIndicatorNode.exitFar(self)

    def enterAt(self):
        pass

    def exitAt(self):
        pass
