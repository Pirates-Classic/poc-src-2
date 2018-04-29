import random

from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pirates.battle.ProjectileAmmo import ProjectileAmmo
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class GrenadeProjectile(ProjectileAmmo):

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
        elif self.ammoSkillId == InventoryType.GrenadeExplosion:
            grenade = loader.loadModelCopy('models/ammunition/cannonball')
            grenade.setScale(0.6)
        else:
            grenade = loader.loadModelCopy('models/ammunition/cannonball')
            if self.ammoSkillId == InventoryType.GrenadeShockBomb:
                grenade.setColorScale(0.2, 1, 0.2, 1)
                grenade.setScale(0.6)
            elif self.ammoSkillId == InventoryType.GrenadeFireBomb:
                grenade.setColorScale(1, 0.2, 0.2, 1)
                grenade.setScale(0.6)
            elif self.ammoSkillId == InventoryType.GrenadeSmokeCloud:
                grenade.setColorScale(0.5, 0.5, 0.5, 1)
                grenade.setScale(0.6)
            elif self.ammoSkillId == InventoryType.GrenadeSiege:
                grenade.setColorScale(0.2, 0.2, 1, 1)
                grenade.setScale(1.5)
        return grenade
