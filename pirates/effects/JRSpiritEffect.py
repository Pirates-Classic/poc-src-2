# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.JRSpiritEffect
import random

from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from pandac.PandaModules import *
from PooledEffect import PooledEffect


class JRSpiritEffect(PooledEffect, EffectController):
    

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModelCopy('models/effects/deathsoul')
        self.effectModel2 = loader.loadModelCopy('models/effects/deathsoul')
        self.effectModel2.reparentTo(self.effectModel)
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.effectModel.setDepthWrite(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.setLightOff()
        self.effectModel.reparentTo(self)
        texture = self.effectModel.findAllTextures()[0]
        texture.setBorderColor(VBase4(0.0, 0.0, 0.0, 0.0))
        texture.setWrapU(Texture.WMBorderColor)
        texture.setWrapV(Texture.WMBorderColor)

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        duration = 3.5
        fadeIn = LerpColorInterval(self, 0.75, Vec4(1.0, 1.0, 1.0, 1.0), startColor=Vec4(1.0, 1.0, 1.0, 0.0))
        fadeOut = LerpColorInterval(self, 1.5, Vec4(1.0, 1.0, 1.0, 0.0), startColor=Vec4(1.0, 1.0, 1.0, 1.0), blendType='easeIn')
        posIval = LerpPosInterval(self.effectModel, duration / 2.5, Vec3(0.0, 0.0, 2.0), startPos=Vec3(0.0, 0.0, 0.0))
        scaleIval = LerpScaleInterval(self, duration, Vec3(1.5, 1.0, 4.0), startScale=Vec3(0.4, 1.0, 0.75))
        uvScrollA = LerpFunctionInterval(self.setNewUVs, duration / 2.5, toData=-2.6, fromData=0.0, extraArgs=[self.effectModel, textureStage])
        uvScrollB = LerpFunctionInterval(self.setNewUVs, duration / 4.5, toData=-6.5, fromData=-2.6, extraArgs=[self.effectModel, textureStage])
        self.startEffect = Parallel(fadeIn, Sequence(Wait(0.5), fadeOut), posIval, scaleIval, Sequence(uvScrollA, uvScrollB))
        self.endEffect = Sequence(Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(duration), self.endEffect)

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        self.stop()
        if self.track:
            self.track = None
        self.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return
# okay decompiling .\pirates\effects\JRSpiritEffect.pyc
