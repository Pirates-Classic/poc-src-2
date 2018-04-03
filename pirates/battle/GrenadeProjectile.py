# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.GrenadeProjectile
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle.ProjectileAmmo import ProjectileAmmo
import random

class GrenadeProjectile(ProjectileAmmo):
    __module__ = __name__

    def __init__(self, cr, ammoSkillId, event):
        ProjectileAmmo.__init__(self, cr, ammoSkillId, event)
        self.splashScale = 1.5
        self.explosionScale = 1.0

    def removeNode(self):
        ProjectileAmmo.removeNode(self)

    def loadModel(self):
        if not base.config.GetBool('want-special-effects', 1):
            grenade = loader.loadModelCopy('models/ammunition/cannonball')
            grenade.setScale(0.6)
        else:
            if self.ammoSkillId == InventoryType.GrenadeExplosion:
                grenade = loader.loadModelCopy('models/ammunition/cannonball')
                grenade.setScale(0.6)
            else:
                grenade = loader.loadModelCopy('models/ammunition/cannonball')
                if self.ammoSkillId == InventoryType.GrenadeShockBomb:
                    grenade.setColorScale(0.2, 1, 0.2, 1)
                    grenade.setScale(0.6)
                else:
                    if self.ammoSkillId == InventoryType.GrenadeFireBomb:
                        grenade.setColorScale(1, 0.2, 0.2, 1)
                        grenade.setScale(0.6)
                    else:
                        if self.ammoSkillId == InventoryType.GrenadeSmokeCloud:
                            grenade.setColorScale(0.5, 0.5, 0.5, 1)
                            grenade.setScale(0.6)
                        else:
                            if self.ammoSkillId == InventoryType.GrenadeSiege:
                                grenade.setColorScale(0.2, 0.2, 1, 1)
                                grenade.setScale(1.5)
        return grenade
# okay decompiling .\pirates\battle\GrenadeProjectile.pyc
