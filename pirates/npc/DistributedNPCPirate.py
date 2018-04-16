# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.DistributedNPCPirate
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pirates.battle import DistributedBattleNPC
from pirates.pirate import DistributedPirateBase
from pirates.piratesbase import PiratesGlobals


class DistributedNPCPirate(DistributedBattleNPC.DistributedBattleNPC, DistributedPirateBase.DistributedPirateBase):
    
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCPirate')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        DistributedPirateBase.DistributedPirateBase.__init__(self, cr)

    def disable(self):
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        DistributedPirateBase.DistributedPirateBase.disable(self)
        self.stopBlink()
        self.ignoreAll()

    def delete(self):
        try:
            self.DistributedNPCPirate_deleted
        except:
            self.DistributedNPCPirate_deleted = 1
            DistributedBattleNPC.DistributedBattleNPC.delete(self)
            DistributedPirateBase.DistributedPirateBase.delete(self)

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        DistributedPirateBase.DistributedPirateBase.generate(self)
        self.setInteractOptions(proximityText=None, allowInteract=False)
        return

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        DistributedPirateBase.DistributedPirateBase.announceGenerate(self)

    def setDNAString(self, dnaString):
        DistributedPirateBase.DistributedPirateBase.setDefaultDNA(self)
        self.style.makeNPCPirate()

    def isBattleable(self):
        return 0

    def play(self, *args, **kwArgs):
        Pirate.Pirate.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        Pirate.Pirate.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        Pirate.Pirate.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Pirate.Pirate.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        Pirate.Pirate.stop(self, *args, **kwArgs)
# okay decompiling .\pirates\npc\DistributedNPCPirate.pyc
