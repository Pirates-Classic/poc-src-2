# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Alligator
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from pirates.creature.Creature import Creature


class Alligator(Creature):
    
    ModelInfo = ('models/char/alligator_hi', 'models/char/alligator_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'death': 'sfx_alligator_death.mp3', 'pain': 'sfx_alligator_flinch_left.mp3'})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('walk', 'walk'), ('run', 'run'), ('swim', 'swim'), ('swim_alt', 'swim_alt'), ('pull_back', 'pull_back'), ('pain', 'pull_back'), ('attack_left', 'attack_left'), ('attack_right', 'attack_right'), ('attack_straight', 'attack_straight'), ('flinch_left', 'flinch_left'), ('flinch_right', 'flinch_right'), ('death', 'death'))

    class AnimationMixer(Creature.AnimationMixer):
        
        notify = DirectNotifyGlobal.directNotify.newCategory('AlligatorAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'walk': (LOOP['LOOP'],), 'run': (LOOP['LOOP'],), 'swim': (LOOP['LOOP'],), 'swim_alt': (LOOP['LOOP'],), 'attack_left': (ACTION['ACTION'],), 'attack_right': (ACTION['ACTION'],), 'attack_straight': (ACTION['ACTION'],), 'pickup_human': (ACTION['ACTION'],), 'flinch_left': (ACTION['ACTION'],), 'flinch_right': (ACTION['ACTION'],), 'pull_back': (ACTION['ACTION'],), 'pain': (ACTION['ACTION'],), 'death': (ACTION['MOVIE'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('swim', 1.0), ('swim', 1.0), ('swim_alt', 1.0), ('swim', -1.0), ('swim_alt', 1.0), ('swim_alt', 1.0), ('swim_alt', 1.0), ('swim_alt', 1.0), ('swim_alt', 1.0), ('swim', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Alligator.sfx:
            for name in Alligator.SfxNames:
                Alligator.sfx[name] = loader.loadSfx('audio/' + Alligator.SfxNames[name])

        self.nametagOffset = 3.8
        self.generateCreature()

    def setupCreature(self):
        DistributedCreature.setupCreature(self)
        texCard = loader.loadModel('models/char/undead_creatures')
        if texCard:
            tex = texCard.findTexture('alligator_undead')
            lodnames = self.getLODNames()
            for lod in lodnames:
                lodptr = self.getLOD(lod)
                lodptr.setTexture(tex, 1)
# okay decompiling .\pirates\creature\Alligator.pyc
