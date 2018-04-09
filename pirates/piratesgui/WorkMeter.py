# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.WorkMeter
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from pandac.PandaModules import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals


class WorkMeter(DirectFrame):
    
    Card = None

    def __init__(self):
        if self.Card == None:
            self.Card = loader.loadModel('models/gui/ship_battle')
        DirectFrame.__init__(self, relief=None, parent=base.a2dBottomCenter, image=self.Card.find('**/ship_battle_speed_bar*'), image_scale=(0.5,
                                                                                                                                             1,
                                                                                                                                             0.8), pos=(0,
                                                                                                                                                        0,
                                                                                                                                                        0.09))
        self.initialiseoptions(WorkMeter)
        self.setName(self.uniqueName('workMeter'))
        self.duration = 0.0
        self.meter = DirectWaitBar(parent=self, relief=DGG.FLAT, text='', text_pos=(0,
                                                                                    0.04), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, range=1.0, value=0.0, frameColor=Vec4(0.2, 0.16, 0.1, 1), barColor=Vec4(1, 0.8, 0.5, 1), pos=(0,
                                                                                                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                                                                                                 0), frameSize=(-0.33, 0.33, -0.0125, 0.0125))
        self.flattenStrong()
        return

    def destroy(self):
        taskMgr.remove(self.taskName('workMeter'))
        DirectFrame.destroy(self)

    def updateText(self, text):
        self.meter['text'] = text

    def update(self, value):
        self.meter['value'] = value

    def startTimer(self, totalTime, timeRemaining=None):
        self.show()
        taskMgr.remove(self.taskName('workMeter'))
        if timeRemaining is None:
            timeRemaining = totalTime
        timeAlreadyElapsed = totalTime - timeRemaining
        self.startSearchTime = globalClock.getFrameTime() - timeAlreadyElapsed
        self.duration = float(totalTime)
        taskMgr.add(self.__updateTimer, self.taskName('workMeter'))
        return

    def __updateTimer(self, task):
        elapsedTime = globalClock.getFrameTime() - self.startSearchTime
        value = elapsedTime / self.duration
        if value >= 1.0:
            self.meter['value'] = 1.0
            return Task.done
        else:
            self.meter['value'] = value
            return Task.cont

    def stopTimer(self):
        taskMgr.remove(self.taskName('workMeter'))
        self.hide()
# okay decompiling .\pirates\piratesgui\WorkMeter.pyc
