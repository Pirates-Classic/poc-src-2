# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestIndicatorNodeArea
from direct.showbase.PythonUtil import StackTrace, report
from pirates.piratesgui.RadarGui import *
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode


class QuestIndicatorNodeArea(QuestIndicatorNode):
    

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'AreaIndicator', [
         100], questStep)
        self.wantBottomEffect = False
        return

    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        QuestIndicatorNode.delete(self)
        return

    def placeInWorld(self):

        def stepObjHere(stepObj):
            self.pendingStepObj = None
            self.reparentTo(stepObj)
            self.setPos(0, 0, 1000)
            self.setHpr(0, 0, 0)
            return

        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        self.pendingStepObj = base.cr.relatedObjectMgr.requestObjects([self.questStep.getStepDoId()], eachCallback=stepObjHere)
        return

    def loadZoneLevel(self, level):
        QuestIndicatorNode.loadZoneLevel(self, level)
        if level == 0:
            self.request('At')
        if level == 1:
            self.request('Far')

    def unloadZoneLevel(self, level):
        QuestIndicatorNode.unloadZoneLevel(self, level)
        if level == 0:
            self.request('Far')
        if level == 1:
            self.request('Off')

    def enterAt(self):
        pass

    def exitAt(self):
        pass

    def enterFar(self):
        QuestIndicatorNode.enterFar(self)
        self.requestTargetRefresh()

    def exitFar(self):
        QuestIndicatorNode.exitFar(self)
        self.stopTargetRefresh()
# okay decompiling .\pirates\quest\QuestIndicatorNodeArea.pyc
