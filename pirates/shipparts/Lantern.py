# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.Lantern
import random

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.destructibles import ShatterableObject
from pirates.effects.LanternGlow import LanternGlow
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesbase.PiratesGlobals import *
from pirates.shipparts import DecorDNA, ShipPart


class Lantern(NodePath, ShatterableObject.ShatterableObject, ShipPart.ShipPart):
    __module__ = __name__
    notify = directNotify.newCategory('Lantern')
    glassBreakSfx = None

    def __init__(self):
        ShatterableObject.ShatterableObject.__init__(self)
        ShipPart.ShipPart.__init__(self)
        NodePath.__init__(self, 'lantern')
        self.isAlive = 1
        self.flash = None
        self.texture = None
        self.lightGlow = None
        self.lanternGlowEffect = None
        if not self.glassBreakSfx:
            self.glassBreakSfx = (
             loader.loadSfx('audio/glass_break1.mp3'), loader.loadSfx('audio/glass_break2.mp3'), loader.loadSfx('audio/glass_break3.mp3'))
        return

    def disable(self):
        ShatterableObject.ShatterableObject.disable(self)
        ShipPart.ShipPart.disable(self)

    def delete(self):
        self.unloadModel()
        ShatterableObject.ShatterableObject.delete(self)
        ShipPart.ShipPart.destroy(self)
        del self.dna
        for i in self.glassBreakSfx:
            i = None

        del self.glassBreakSfx
        self.clearTargetableCollisions()
        return

    def loadModel(self, dna):
        if config.GetBool('disable-ship-geom', 0):
            return
        if self.prop:
            return
        self.dna = dna
        filePrefix = self.getPrefix(self.dna.decorType, self.dna.baseTeam)
        self.prop = loader.loadModelCopy(filePrefix[0])
        self.geom_Low = NodePath('low')
        lightHigh = self.prop.find('**/light_High')
        if not lightHigh.isEmpty():
            lightHigh.flattenStrong()
            self.geom_High = lightHigh.find('**/+GeomNode')
        else:
            self.geom_High = NodePath('hi')
        lightMed = self.prop.find('**/light_Med')
        if not lightMed.isEmpty():
            lightMed.flattenStrong()
            self.geom_Medium = lightMed.find('**/+GeomNode')
        else:
            self.geom_Medium = NodePath('med')
        self.propCollisions = self.attachNewNode('Lantern-%d' % self.dna.posIndex)
        self.prop.flattenMedium()
        self.initializeDebris(wantHidden=1, wantRotate=1)
        self.coll = self.prop.findAllMatches('**/collisions/*').asList()
        for c in self.coll:
            c.setTag('objType', str(PiratesGlobals.COLL_SHIPPART))
            c.setTag('propId', str(self.doId))
            c.setTag('cannonPass', str(1))
            c.setTag('shipId', str(self.shipId))
            c.node().setIntoCollideMask(BitMask32().allOff())
            c.node().setFromCollideMask(BitMask32().allOff())
            self.addTargetableCollision(c)
            c.reparentTo(self.propCollisions)

        self.setTargetBitmask(1)
        self.discs = []
        self.lights = []
        lightCol = [
         VBase4(1, 1, 0.8, 1), VBase4(0, 0, 1, 1), VBase4(0, 1, 0, 1), VBase4(1, 0, 0, 1)]
        plight = self.prop.find('**/polylight*')
        if not plight.isEmpty():
            plight.detachNode()
        self.loaded = True

    def unloadModel(self):
        if not self.prop:
            return
        if self.flash:
            self.flash.pause()
            self.flash = None
        ShatterableObject.ShatterableObject.disable(self)
        if self.propCollisions:
            self.propCollisions.removeNode()
            self.propCollisions = None
        if self.prop:
            self.prop.removeNode()
            self.prop = None
        for i in self.discs:
            i.destroy()

        self.discs = []
        for i in self.lights:
            i.removeNode()

        self.lights = []
        self.removeNode()
        return

    def getPrefix(self, shipClass, team):
        filePrefix = None
        if team == PiratesGlobals.UNDEAD_TEAM:
            filePrefix = DecorDNA.SkelDecorDict.get(shipClass)
        else:
            if team == PiratesGlobals.FRENCH_UNDEAD_TEAM or team == PiratesGlobals.SPANISH_UNDEAD_TEAM:
                filePrefix = DecorDNA.SkelDecorDict.get(shipClass)
            else:
                filePrefix = DecorDNA.DecorDict.get(shipClass)
        return filePrefix

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        sfx = random.choice(self.glassBreakSfx)
        base.playSfx(sfx, node=self, cutoff=2500)

    def death(self):
        if self.prop and self.isAlive:
            self.showBrokenState()
            self.playBreakAll()

    def showBrokenState(self):
        self.isAlive = 0
        self.setTargetBitmask(0)

    def respawn(self):
        if self.isAlive == 0:
            self.isAlive = 1
            if self.prop != None:
                if base.localAvatar.ship != self.ship:
                    self.setTargetBitmask(1)
                self.lighGlow.unstash()
                self.resetDebris()
        return

    def playFlash(self):
        if self.flash:
            self.flash.finish()
            self.flash = None
        self.flash = Sequence(Func(self.hideBaseTexture), Func(self.prop.setColor, Vec4(1, 1, 0, 1)), Wait(0.03), Func(self.prop.setColor, Vec4(1, 0, 0, 1)), Wait(0.03), Func(self.prop.setColorOff), Func(self.showBaseTexture), Wait(0.1), Func(self.hideBaseTexture), Func(self.prop.setColor, Vec4(1, 1, 0, 1)), Wait(0.03), Func(self.prop.setColor, Vec4(1, 0, 0, 1)), Wait(0.03), Func(self.prop.setColorOff), Func(self.showBaseTexture))
        self.flash.start()
        return

    def hideBaseTexture(self):
        if not self.texture:
            self.textures = self.prop.findTexture('*')
        ts = self.prop.findAllTextureStages()
        if ts.getNumTextureStages():
            self.prop.setTextureOff(ts[0])

    def showBaseTexture(self):
        if self.textures:
            self.prop.setTexture(self.textures, 1)
# okay decompiling .\pirates\shipparts\Lantern.pyc
