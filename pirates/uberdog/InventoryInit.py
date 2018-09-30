from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory

UberDogRevision = 1

CategoryLimits = {
    InventoryCategory.QUESTS: 255,
    InventoryCategory.MONEY: 7,
    InventoryCategory.MAX_PLAYER_ATTRIBUTES: 2,
    InventoryCategory.WEAPONS: 100,
    InventoryCategory.WEAPON_SKILL_MELEE: 100,
    InventoryCategory.WEAPON_SKILL_CUTLASS: 100,
    InventoryCategory.WEAPON_SKILL_PISTOL: 100,
    InventoryCategory.WEAPON_SKILL_MUSKET: 100,
    InventoryCategory.WEAPON_SKILL_DAGGER: 100,
    InventoryCategory.WEAPON_SKILL_GRENADE: 100,
    InventoryCategory.WEAPON_SKILL_DOLL: 100,
    InventoryCategory.WEAPON_SKILL_WAND: 100,
    InventoryCategory.WEAPON_SKILL_KETTLE: 100,
    InventoryCategory.WEAPON_SKILL_CANNON: 100,
    InventoryCategory.WEAPON_SKILL_ITEM: 100,
    InventoryCategory.SKILL_SAILING: 100,
    InventoryCategory.WAGERS: 100,
    InventoryCategory.KEY_ITEMS: 30,
    InventoryCategory.TELEPORT_TOKENS: 30,
    InventoryCategory.CONSUMABLES: 50,
    InventoryCategory.SHIPS: 3,
    InventoryCategory.SHIP_ACCESSORIES: 250,
    InventoryCategory.SHIP_CANNONS: 200,
    InventoryCategory.FLAGS: 5,
    InventoryCategory.COLLECTIONS: 250,
    InventoryCategory.FISH_CAUGHT: 20,
    InventoryCategory.TREASURE_MAPS: 3,
    InventoryCategory.QUEST_SLOTS: 255,
    InventoryCategory.ACCUMULATORS: 20,
    InventoryCategory.REPAIR_TOKENS: 2,
    InventoryCategory.WEAPON_PISTOL_AMMO: 200,
    InventoryCategory.WEAPON_MUSKET_AMMO: 200,
    InventoryCategory.WEAPON_GRENADE_AMMO: 200,
    InventoryCategory.WEAPON_CANNON_AMMO: 200,
    InventoryCategory.WEAPON_DAGGER_AMMO: 200,
    InventoryCategory.UNSPENT_SKILL_POINTS: 100,
    InventoryCategory.VITAE_PENALTY: 10000,
    InventoryCategory.PLAYER_RANKING: 10000,
    InventoryCategory.CARDS: 100,
    InventoryCategory.PISTOL_POUCHES: 10,
    InventoryCategory.DAGGER_POUCHES: 10,
    InventoryCategory.GRENADE_POUCHES: 10,
    InventoryCategory.CANNON_POUCHES: 10,
    InventoryCategory.SONGS: 100,
    InventoryCategory.NUM_RESPEC: 20,
    InventoryCategory.PVP_RENOWN: 10,
}

StackLimits = {
    InventoryType.MeleePunch: 6,
    InventoryType.MeleeKick: 6,
    InventoryType.SailBroadsideLeft: 6,
    InventoryType.SailBroadsideRight: 6,
    InventoryType.SailFullSail: 6,
    InventoryType.SailComeAbout: 6,
    InventoryType.SailOpenFire: 6,
    InventoryType.SailRammingSpeed: 6,
    InventoryType.SailTakeCover: 6,
    InventoryType.SailWindcatcher: 6,
    InventoryType.SailTacking: 6,
    InventoryType.SailPowerRecharge: 2,
    InventoryType.CutlassHack: 6,
    InventoryType.CutlassSlash: 6,
    InventoryType.CutlassSweep: 6,
    InventoryType.DaggerCut: 6,
    InventoryType.DaggerSwipe: 6,
    InventoryType.AmmoAsp: 100,
    InventoryType.AmmoAdder: 50,
    InventoryType.AmmoSidewinder: 50,
    InventoryType.AmmoViperNest: 25,
    InventoryType.PistolShoot: 6,
    InventoryType.PistolLeadShot: 6,
    InventoryType.AmmoLeadShot: 6,
    InventoryType.AmmoBaneShot: 100,
    InventoryType.AmmoSilverShot: 100,
    InventoryType.AmmoHexEaterShot: 100,
    InventoryType.AmmoSteelShot: 100,
    InventoryType.AmmoVenomShot: 100,
    InventoryType.CannonShoot: 6,
    InventoryType.CannonRoundShot: 6,
    InventoryType.CannonGrappleHook: 6,
    InventoryType.AmmoRoundShot: 1,
    InventoryType.AmmoChainShot: 100,
    InventoryType.AmmoExplosive: 3,
    InventoryType.AmmoGrapeShot: 100,
    InventoryType.AmmoFirebrand: 50,
    InventoryType.AmmoThunderbolt: 50,
    InventoryType.AmmoFury: 50,
    InventoryType.AmmoGrappleHook: 100,
    InventoryType.DollAttune: 6,
    InventoryType.DollPoke: 6,
    InventoryType.StaffBlast: 6,
    InventoryType.StaffSoulFlay: 6,
    InventoryType.GrenadeThrow: 6,
    InventoryType.GrenadeExplosion: 6,
    InventoryType.AmmoGrenadeExplosion: 75,
    InventoryType.AmmoGrenadeShockBomb: 50,
    InventoryType.AmmoGrenadeFlame: 50,
    InventoryType.AmmoGrenadeSmoke: 25,
    InventoryType.AmmoGrenadeLandMine: 25,
    InventoryType.AmmoGrenadeSiege: 25,
    InventoryType.PistolPouchL1: 1,
    InventoryType.PistolPouchL2: 1,
    InventoryType.PistolPouchL3: 1,
    InventoryType.DaggerPouchL1: 1,
    InventoryType.DaggerPouchL2: 1,
    InventoryType.DaggerPouchL3: 1,
    InventoryType.GrenadePouchL1: 1,
    InventoryType.GrenadePouchL2: 1,
    InventoryType.GrenadePouchL3: 1,
    InventoryType.CannonPouchL1: 1,
    InventoryType.CannonPouchL2: 1,
    InventoryType.CannonPouchL3: 1,
    InventoryType.UnspentMelee: 50,
    InventoryType.UnspentCutlass: 50,
    InventoryType.UnspentDagger: 50,
    InventoryType.UnspentGrenade: 50,
    InventoryType.UnspentWand: 50,
    InventoryType.UnspentDoll: 50,
    InventoryType.UnspentCannon: 50,
    InventoryType.UnspentPistol: 50,
    InventoryType.UnspentSailing: 50,
    InventoryType.Vitae_Level: 100,
    InventoryType.Vitae_Cost: 10000,
    InventoryType.Vitae_Left: 10000,
    InventoryType.Vitae_Update: 10000,
    InventoryType.UseItem: 6,
    InventoryType.CTFGame: 9999,
    InventoryType.CTLGame: 9999,
    InventoryType.PTRGame: 9999,
    InventoryType.BTLGame: 9999,
    InventoryType.TBTGame: 9999,
    InventoryType.SBTGame: 9999,
    InventoryType.ARMGame: 9999,
    InventoryType.TKPGame: 9999,
    InventoryType.BTBGame: 9999,
    InventoryType.PokerGame: 9999,
    InventoryType.BlackjackGame: 9999,
    InventoryType.ShipPVPRank: 9999,
    InventoryType.PVPTotalInfamyLand: 10000,
    InventoryType.PVPCurrentInfamy: 50000,
    InventoryType.PVPTotalInfamySea: 10000,
    InventoryType.Collection_Set1: 2,
    InventoryType.Collection_Set1_Part1: 99,
    InventoryType.Collection_Set1_Part2: 99,
    InventoryType.Collection_Set1_Part3: 99,
    InventoryType.Collection_Set1_Part4: 99,
    InventoryType.Collection_Set1_Part5: 99,
    InventoryType.Collection_Set1_Part6: 99,
    InventoryType.Collection_Set1_Part7: 99,
    InventoryType.Collection_Set1_Part8: 99,
    InventoryType.Collection_Set1_Part9: 99,
    InventoryType.Collection_Set1_Part10: 99,
    InventoryType.Collection_Set1_Part11: 99,
    InventoryType.Collection_Set1_Part12: 99,
    InventoryType.Collection_Set1_Part13: 99,
    InventoryType.Collection_Set1_Part14: 99,
    InventoryType.Collection_Set1_Part15: 99,
    InventoryType.Collection_Set1_Part16: 99,
    InventoryType.Collection_Set1_Part17: 99,
    InventoryType.Collection_Set1_Part18: 99,
    InventoryType.Collection_Set1_Part19: 99,
    InventoryType.Collection_Set1_Part20: 99,
    InventoryType.Collection_Set2: 2,
    InventoryType.Collection_Set2_Part1: 99,
    InventoryType.Collection_Set2_Part2: 99,
    InventoryType.Collection_Set2_Part3: 99,
    InventoryType.Collection_Set2_Part4: 99,
    InventoryType.Collection_Set2_Part5: 99,
    InventoryType.Collection_Set2_Part6: 99,
    InventoryType.Collection_Set2_Part7: 99,
    InventoryType.Collection_Set2_Part8: 99,
    InventoryType.Collection_Set2_Part9: 99,
    InventoryType.Collection_Set2_Part10: 99,
    InventoryType.Collection_Set2_Part11: 99,
    InventoryType.Collection_Set2_Part12: 99,
    InventoryType.Collection_Set2_Part13: 99,
    InventoryType.Collection_Set2_Part14: 99,
    InventoryType.Collection_Set2_Part15: 99,
    InventoryType.Collection_Set2_Part16: 99,
    InventoryType.Collection_Set2_Part17: 99,
    InventoryType.Collection_Set2_Part18: 99,
    InventoryType.Collection_Set2_Part19: 99,
    InventoryType.Collection_Set2_Part20: 99,
    InventoryType.Collection_Set3: 2,
    InventoryType.Collection_Set3_Part1: 99,
    InventoryType.Collection_Set3_Part2: 99,
    InventoryType.Collection_Set3_Part3: 99,
    InventoryType.Collection_Set3_Part4: 99,
    InventoryType.Collection_Set3_Part5: 99,
    InventoryType.Collection_Set3_Part6: 99,
    InventoryType.Collection_Set3_Part7: 99,
    InventoryType.Collection_Set3_Part8: 99,
    InventoryType.Collection_Set3_Part9: 99,
    InventoryType.Collection_Set4: 2,
    InventoryType.Collection_Set4_Part1: 99,
    InventoryType.Collection_Set4_Part2: 99,
    InventoryType.Collection_Set4_Part3: 99,
    InventoryType.Collection_Set4_Part4: 99,
    InventoryType.Collection_Set4_Part5: 99,
    InventoryType.Collection_Set4_Part6: 99,
    InventoryType.Collection_Set4_Part7: 99,
    InventoryType.Collection_Set4_Part8: 99,
    InventoryType.Collection_Set4_Part9: 99,
    InventoryType.Collection_Set4_Part10: 99,
    InventoryType.Collection_Set4_Part11: 99,
    InventoryType.Collection_Set4_Part12: 99,
    InventoryType.Collection_Set4_Part13: 99,
    InventoryType.Collection_Set4_Part14: 99,
    InventoryType.Collection_Set5: 2,
    InventoryType.Collection_Set5_Part1: 99,
    InventoryType.Collection_Set5_Part2: 99,
    InventoryType.Collection_Set5_Part3: 99,
    InventoryType.Collection_Set5_Part4: 99,
    InventoryType.Collection_Set5_Part5: 99,
    InventoryType.Collection_Set5_Part6: 99,
    InventoryType.Collection_Set5_Part7: 99,
    InventoryType.Collection_Set6: 2,
    InventoryType.Collection_Set6_Part1: 99,
    InventoryType.Collection_Set6_Part2: 99,
    InventoryType.Collection_Set6_Part3: 99,
    InventoryType.Collection_Set6_Part4: 99,
    InventoryType.Collection_Set6_Part5: 99,
    InventoryType.Collection_Set6_Part6: 99,
    InventoryType.Collection_Set6_Part7: 99,
    InventoryType.Collection_Set6_Part8: 99,
    InventoryType.Collection_Set6_Part9: 99,
    InventoryType.Collection_Set6_Part10: 99,
    InventoryType.Collection_Set6_Part11: 99,
    InventoryType.Collection_Set7: 2,
    InventoryType.Collection_Set7_Part1: 99,
    InventoryType.Collection_Set7_Part2: 99,
    InventoryType.Collection_Set7_Part3: 99,
    InventoryType.Collection_Set7_Part4: 99,
    InventoryType.Collection_Set7_Part5: 99,
    InventoryType.Collection_Set7_Part6: 99,
    InventoryType.Collection_Set7_Part7: 99,
    InventoryType.Collection_Set7_Part8: 99,
    InventoryType.Collection_Set7_Part9: 99,
    InventoryType.Collection_Set7_Part10: 99,
    InventoryType.Collection_Set7_Part11: 99,
    InventoryType.Collection_Set7_Part12: 99,
    InventoryType.Collection_Set8: 2,
    InventoryType.Collection_Set8_Part1: 99,
    InventoryType.Collection_Set8_Part2: 99,
    InventoryType.Collection_Set8_Part3: 99,
    InventoryType.Collection_Set8_Part4: 99,
    InventoryType.Collection_Set8_Part5: 99,
    InventoryType.Collection_Set8_Part6: 99,
    InventoryType.Collection_Set8_Part7: 99,
    InventoryType.Collection_Set8_Part8: 99,
    InventoryType.Collection_Set8_Part9: 99,
    InventoryType.Collection_Set8_Part10: 99,
    InventoryType.Collection_Set8_Part11: 99,
    InventoryType.Collection_Set8_Part12: 99,
    InventoryType.Collection_Set8_Part13: 99,
    InventoryType.Collection_Set8_Part14: 99,
    InventoryType.Collection_Set8_Part15: 99,
    InventoryType.Collection_Set9: 1,
    InventoryType.Collection_Set9_Part1: 1,
    InventoryType.Collection_Set9_Part2: 1,
    InventoryType.Collection_Set9_Part3: 1,
    InventoryType.Collection_Set9_Part4: 1,
    InventoryType.Collection_Set9_Part5: 1,
    InventoryType.Collection_Set9_Part6: 1,
    InventoryType.Collection_Set9_Part7: 1,
    InventoryType.Collection_Set9_Part8: 1,
    InventoryType.Collection_Set9_Part9: 1,
    InventoryType.Collection_Set9_Part10: 1,
    InventoryType.Collection_Set9_Part11: 1,
    InventoryType.Collection_Set9_Part12: 1,
    InventoryType.Collection_Set10: 1,
    InventoryType.OpenQuestSlot: 255,
    InventoryType.NewPlayerToken: 1,
    InventoryType.NewWeaponToken: 1,
    InventoryType.NewShipToken: 1,
    InventoryType.Dinghy: 1,
    InventoryType.SmallBottle: 5,
    InventoryType.MediumBottle: 5,
    InventoryType.LargeBottle: 5,
    InventoryType.CutlassToken: 1,
    InventoryType.PistolToken: 1,
    InventoryType.MusketToken: 1,
    InventoryType.DaggerToken: 1,
    InventoryType.GrenadeToken: 1,
    InventoryType.WandToken: 1,
    InventoryType.DollToken: 1,
    InventoryType.KettleToken: 1,
    InventoryType.FirstDeathToken: 1,
    InventoryType.TortugaTeleportToken: 1,
    InventoryType.PortRoyalTeleportToken: 1,
    InventoryType.KingsheadTeleportToken: 1,
    InventoryType.PadresDelFuegoTeleportToken: 1,
    InventoryType.CubaTeleportToken: 1,
    InventoryType.PlayerHealToken: 1000,
    InventoryType.PlayerMojoHealToken: 1000,
    InventoryType.NumRespecCutlass: 32767,
    InventoryType.NumRespecPistol: 32767,
    InventoryType.NumRespecDoll: 32767,
    InventoryType.NumRespecDagger: 32767,
    InventoryType.NumRespecGrenade: 32767,
    InventoryType.NumRespecStaff: 32767,
    InventoryType.NumRespecCannon: 32767,
    InventoryType.NumRespecSailing: 32767,
    InventoryType.PvPRenownLand: 10000,
    InventoryType.PvPRenownSea: 10000,
    InventoryType.PvPPointsLand: 10000,
    InventoryType.PvPPointsSea: 10000,
}

for i in range(52):
    stack_limit = 100
    StackLimits[InventoryType.begin_Cards + i] = stack_limit

for i in range(InventoryType.begin_Songs, InventoryType.end_Songs):
    StackLimits[i] = 1

StartingStacks = {
    # Weapons
    InventoryType.CutlassWeaponL1: 0,
    InventoryType.PistolWeaponL1: 0,
    InventoryType.MusketWeaponL1: 0,
    InventoryType.BayonetWeaponL1: 0,
    InventoryType.DaggerWeaponL1: 0,
    InventoryType.GrenadeWeaponL1: 0,
    InventoryType.DollWeaponL1: 0,
    InventoryType.WandWeaponL1: 0,

    # Skills
    InventoryType.CannonShoot: 2,
    InventoryType.CannonRoundShot: 2,
    InventoryType.SailBroadsideLeft: 2,
    InventoryType.SailBroadsideRight: 2,
    InventoryType.CutlassSweep: 1,

    # Skill Points
    InventoryType.UnspentCutlass: 1,

    # Weapon Tokens
    InventoryType.CutlassToken: 1,
    InventoryType.FirstDeathToken: 1,

    # Teleport Tokens
    InventoryType.TortugaTeleportToken: 0,
    InventoryType.PortRoyalTeleportToken: 1,
    InventoryType.KingsheadTeleportToken: 0,
    InventoryType.PadresDelFuegoTeleportToken: 0,
    InventoryType.CubaTeleportToken: 0,

    # Music
    InventoryType.Song_1: 1,
    InventoryType.Song_2: 1,
    InventoryType.Song_3: 1,
    InventoryType.Song_4: 1,
    InventoryType.Song_5: 1,
}

AccumulatorLimits = {
    InventoryType.OverallRep: 540150,
    InventoryType.GeneralRep: 56600,
    InventoryType.MeleeRep: 56600,
    InventoryType.CutlassRep: 56600,
    InventoryType.PistolRep: 56600,
    InventoryType.MusketRep: 56600,
    InventoryType.DaggerRep: 56600,
    InventoryType.GrenadeRep: 56600,
    InventoryType.WandRep: 56600,
    InventoryType.DollRep: 56600,
    InventoryType.KettleRep: 56600,
    InventoryType.CannonRep: 56600,
    InventoryType.SailingRep: 56600,
    InventoryType.MonsterRep: 56600,
    InventoryType.LockpickRep: 56600,
    InventoryType.GamblingRep: 56600,
}
