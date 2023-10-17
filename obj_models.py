# -*- coding: utf-8 -*-

# Nom de surface,  Animation,  Forme,  Genre (Solide, Danger),  Solidite,  Hitbox,  SpecialSprites,  VirtualSpecials
map_object_models = {

"invisible_element": # Objet de niveau 0
{"name":None, "sh":0, "k":(False, False), "h":-1, "hb":0, "pts":0,
"spe":{"zoneSignal":{"m":2, "tar":"-", "signalOn":"-", "signalOff":"-"}}},

"start": # Objet de niveau 0
{"name":"start", "sh":1, "k":(False, False), "h":-1, "hb":0, "pts":0,
"spe":{}},

"exit": # Objet de niveau max
{"name":"exit", "sh":1, "k":(False, False), "h":-1, "hb":40, "pts":0,
"spe":{"anim":{"f":15}}},

"largeWall": # Objet de niveau 5
{"name":"largeWall", "sh":0, "k":(True, False), "h":-1, "hb":0, "pts":0,
"spe":{}},

"blackBlock": # Objet de niveau 0
{"name":None, "sh":0, "k":(True, False), "h":-1, "hb":0, "pts":0,
"spe":{"colorShape":{"r":0, "v":0, "b":0, "w":100, "h":100}}},

"smallWall": # Objet de niveau 3
{"name":"smallWall", "sh":0, "k":(True, False), "h":-1, "hb":0, "pts":0,
"spe":{}},

"smallSquare": # Objet de niveau 3
{"name":"smallSquare", "sh":0, "k":(True, False), "h":-1, "hb":0, "pts":0,
"spe":{}},

"wood_block": # Objet de niveau 2
{"name":"wood_block", "sh":0, "k":(True, False), "h":80, "hb":0, "pts":0,
"spe":{}},

"glassBlock": # Objet de niveau 1
{"name":"glassBlock", "sh":0, "k":(True, False), "h":20, "hb":0, "pts":0,
"spe":{"randRot":{"range":90}}},

"spikes": # Objet de niveau 5
{"name":"spikes", "sh":0, "k":(False, True), "h":-1, "hb":-12, "pts":0,
"spe":{"randRot":{"range":90}}},

"round_spikes": # Objet de niveau 4
{"name":"round_spikes", "sh":1, "k":(False, True), "h":-1, "hb":-12, "pts":0,
"spe":{"randRot":{"range":10}}},

"spike_square": # Objet de niveau 5
{"name":"spike_square", "sh":0, "k":(True, True), "h":-1, "hb":-9, "pts":0,
"spe":{"randRot":{"range":90}}},

"standartTurret": # Objet de niveau 10
{"name":"turret", "sh":0, "k":(True, True), "h":185, "hb":0, "pts":10,
"spe":{"shooting":{"p":"redBullet", "s":0, "cd":30, "r":360, "alwSh":False, "sm":False}}},

"blueTurret": # Objet de niveau 11
{"name":"turret", "sh":0, "k":(True, True), "h":185, "hb":0, "pts":10,
"spe":{"shooting":{"p":"blueBullet", "s":0, "cd":60, "r":360, "alwSh":False, "sm":False}}},

"bombTurret": # Objet de niveau 24
{"name":"turret", "sh":0, "k":(True, True), "h":225, "hb":0, "pts":13,
"spe":{"shooting":{"p":"bomb", "s":0, "cd":120, "r":360, "alwSh":False, "sm":False}}},

"duoTurret": # Objet de niveau 25
{"name":"turret", "sh":0, "k":(True, True), "h":250, "hb":0, "pts":15,
"spe":{"duo_shooting":{"p":"whiteBullet2", "s":0, "r":360, "cd":5, "speed":4}}},

"softTurret": # Objet de niveau 8
{"name":"turret", "sh":0, "k":(True, True), "h":160, "hb":0, "pts":7,
"spe":{"shooting":{"p":"whiteBullet", "s":0, "r":360, "cd":70, "alwSh":False, "sm":False}}},

"multipleShootTurret": # Objet de niveau 13
{"name":"turret", "sh":0, "k":(True, True), "h":200, "hb":0, "pts":12,
"spe":{"multipleShooting":{"p":"fireball", "s":3, "r":360, "cd":60, "alwSh":False, "sm":False}}},

"techTurret": # Objet de niveau 11
{"name":"turret", "sh":0, "k":(True, True), "h":185, "hb":0, "pts":10,
"spe":{"randShoot":{"p":"energyOrb", "s":5, "r":360, "cd":20, "alwSh":False, "sm":False}}},

"arrowTurret": # Objet de niveau 12
{"name":"turret", "sh":0, "k":(True, True), "h":185, "hb":0, "pts":10,
"spe":{"shooting":{"p":"greenArrow", "s":10, "cd":10, "r":360, "alwSh":False, "sm":False}}},

"b-arcTurret": # Objet de niveau 15
{"name":"turret", "sh":0, "k":(True, True), "h":200, "hb":0, "pts":12,
"spe":{"shooting":{"p":"bouncingArc", "s":0, "cd":90, "r":360, "alwSh":True, "sm":False}}},

"sniperTurret": # Objet de niveau 22
{"name":"turret", "sh":0, "k":(True, True), "h":250, "hb":0, "pts":14,
"spe":{"shooting":{"p":"real_bullet", "s":0, "r":150, "cd":100, "alwSh":False, "sm":True}}},

"g-follTurret": # Objet de niveau 16
{"name":"turret", "sh":0, "k":(True, True), "h":200, "hb":0, "pts":12,
"spe":{"shooting":{"p":"greenFollower", "s":0, "r":360, "cd":100, "alwSh":True, "sm":False}}},

"ghostTurret": # Objet de niveau 19
{"name":"turret", "sh":0, "k":(True, True), "h":200, "hb":0, "pts":13,
"spe":{"randShoot":{"p":"ghostBullet", "s":0, "r":360, "cd":50, "alwSh":True, "sm":False}}},

"sequenceTurret": # Objet de niveau 10
{"name":"turret", "sh":0, "k":(True, True), "h":185, "hb":0, "pts":10,
"spe":{"seqShoot":{"p":"redBullet", "s":7, "r":360, "cd":80, "alwSh":False, "sm":False}}},

"lazerTurret": # Objet de niveau 30
{"name":"laz_turret", "sh":1, "k":(True, True), "h":300, "hb":0, "pts":18,
"spe":{"lazer":{"s":2, "r":360, "m":0, "sq":False, "on":True, "rot":1}}},

"lazerCube": # Objet de niveau 15
{"name":"laz_square", "sh":0, "k":(True, False), "h":-1, "hb":0, "pts":0,
"spe":{"lazer":{"s":0, "r":360, "m":0, "sq":True, "on":True, "rot":0}}},

"pylone": # Objet de niveau 4
{"name":"pylone", "sh":1, "k":(True, False), "h":-1, "hb":0, "pts":0,
"spe":{"randRot":{"range":10}}},

"wood_cone": # Objet de niveau 2
{"name":"wood_cone", "sh":1, "k":(True, False), "h":70, "hb":0, "pts":0,
"spe":{"randRot":{"range":10}}},

"spiky_wood": # Objet de niveau 4
{"name":"spiky_wood", "sh":0, "k":(True, True), "h":95, "hb":-5, "pts":0,
"spe":{}},

"spiky_wheel": # Objet de niveau 3
{"name":"spiky_wheel", "sh":1, "k":(True, True), "h":90, "hb":-12, "pts":0,
"spe":{"rotate":{"s":-5, "r":True}}},

"glass_cone": # Objet de niveau 1
{"name":"glass_cone", "sh":1, "k":(True, False), "h":16, "hb":0, "pts":0,
"spe":{"randRot":{"range":10}}},

"star": # Objet de niveau 35
{"name":"star", "sh":1, "k":(True, True), "h":300, "hb":0, "pts":20,
"spe":{"megaShoot":{"p":"whiteBullet2", "cd":60, "nb":9}, "rotate":{"s":-3, "r":True}}},

"saw": # Objet de niveau 5
{"name":"circularSaw", "sh":1, "k":(True, True), "h":-1, "hb":-23, "pts":0,
"spe":{"rotate":{"s":-25, "r":False}}},

"contact_button": # Objet de niveau 7
{"name":"square_button", "sh":0, "k":(False, False), "h":-1, "hb":-14, "pts":0,
"spe":{"zoneSignal":{"m":0, "tar":"-", "signalOn":"-", "signalOff":"-"},
"contact_button":{"m":0}}},

"door": # Objet de niveau 10
{"name":"door", "sh":0, "k":(True, False), "h":-1, "hb":-8, "pts":0,
"spe":{"door":{}}},

"teleporter": # Objet de niveau 27
{"name":"teleporter", "sh":1, "k":(False, False), "h":-1, "hb":-15, "pts":0,
"spe":{"tp":{"pos":[(100, 100)], "sUse":False}, "rotate":{"s":6, "r":True}}},

"small_magicWall": # Objet de niveau 12
{"name":"small_magicWall", "sh":0, "k":(False, False), "h":-1, "hb":0, "pts":0,
"spe":{"forceField":{}}},

"med_magicWall": # Objet de niveau 15
{"name":"med_magicWall", "sh":0, "k":(False, False), "h":-1, "hb":0, "pts":0,
"spe":{"forceField":{}}},

"large_magicWall": # Objet de niveau 20
{"name":"large_magicWall", "sh":0, "k":(False, False), "h":-1, "hb":0, "pts":0,
"spe":{"forceField":{}}},

"screenBlock": # Objet de niveau 2
{"name":"screenBlock", "sh":0, "k":(False, False), "h":-1, "hb":0, "pts":0,
"spe":{"signalCondition":{"nb":3, "tar":"-", "signal":"-", "show":True}}},

"spike_wall": # Objet de niveau 5
{"name":"spike_wall", "sh":0, "k":(True, True), "h":-1, "hb":-1, "pts":0,
"spe":{}},

"ring": # Objet de niveau 20
{"name":"a-ring", "sh":1, "k":(False, False), "h":-1, "hb":0, "pts":0,
"spe":{"point":{}}},

"teslaTurret": # Objet de niveau 30
{"name":"tesla", "sh":1, "k":(True, False), "h":-1, "hb":0, "pts":0,
"spe":{"tesla":{"scope":300, "load":60, "on":True}}},
}

specials_default = {

"anim":map_object_models["exit"]["spe"]["anim"],
"colorShape":map_object_models["blackBlock"]["spe"]["colorShape"],
"randRot":map_object_models["glassBlock"]["spe"]["randRot"],
"shooting":map_object_models["standartTurret"]["spe"]["shooting"],
"multipleShooting":map_object_models["multipleShootTurret"]["spe"]["multipleShooting"],
"randShoot":map_object_models["techTurret"]["spe"]["randShoot"],
"seqShoot":map_object_models["sequenceTurret"]["spe"]["seqShoot"],
"lazer":map_object_models["lazerTurret"]["spe"]["lazer"],
"megaShoot":map_object_models["star"]["spe"]["megaShoot"],
"rotate":map_object_models["star"]["spe"]["rotate"],
"destroySignal":{"signal":"-", "tar":"-"},
"hitSignal":{"signal":"-", "tar":"-"},
"zoneSignal":map_object_models["contact_button"]["spe"]["zoneSignal"],
"clockSignal":{"signalOn":"-", "signalOff":"-", "tar":"-", "p1":60, "p2":60},
"contact_button":map_object_models["contact_button"]["spe"]["contact_button"],
"door":map_object_models["door"]["spe"]["door"],
"teleporter":map_object_models["teleporter"]["spe"]["tp"],
"moving":{"pos":[(100, 100), (300, 100), (300, 300), (100, 300)], "s":5, "active":True, "start":0, "p1":-1, "p2":-1, "p3":-1, "p4":-1, "p5":-1},
"orbit":{"cen":[(683, 384)], "s":2, "active":True},
"signalCondition":map_object_models["screenBlock"]["spe"]["signalCondition"],
"duo_shooting":map_object_models["duoTurret"]["spe"]["duo_shooting"],
"tesla":map_object_models["teslaTurret"]["spe"]["tesla"],
"follMove":{"tar":"-"},
"delaySignal":{"t":1, "signal":"-", "tar":"-"},
"focusable":{},
}
