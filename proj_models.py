# -*- coding: utf-8 -*-

# Numero/Nom,  Degats,  Vitesse,  Ratio,  Texture,  Effet de destruction,  Particules,  Speciaux
projectile_models = {\
\
"whiteArrow":\
{"n":0, "dmg":24, "s":15, "r":16, "des":"a-miniExplosion", "dest":18, \
"tr":{"n":5, "f":10, "c":(255, 255, 255), "o":150, "z":5, "d":1}, "spe":{}, "sound":"shoot1"}, \
\
"blueFragment":\
{"n":1, "dmg":8, "s":17, "r":13, "des":"a-star", "dest":15, \
"tr":{"n":1, "f":6, "c":(100, 255, 255), "o":255, "z":1, "d":1}, "spe":{}, "sound":"shoot2"}, \
\
"redBullet":\
{"n":2, "dmg":-1, "s":8, "r":12, "des":"a-redDestruction", "dest":20, \
"tr":{"n":2, "f":12, "c":(255, 0, 0), "o":200, "z":5, "d":0}, "spe":{}, "sound":"turretShoot1"}, \
\
"fireball":\
{"n":3, "dmg":-1, "s":5, "r":18, "des":"a-fireBallOff", "dest":18, \
"tr":{"n":2, "f":24, "c":(255, 150, 0), "o":200, "z":8, "d":1}, "spe":{}, "sound":"turretShoot2"}, \
\
"energyOrb":\
{"n":4, "dmg":-1, "s":7, "r":12, "des":"a-electricity", "dest":9, \
"tr":{"n":1, "f":10, "c":(200, 200, 255), "o":150, "z":5, "d":1}, "spe":{"unstable":{"u":3}}, "sound":"engShoot"}, \
\
"whiteBullet":\
{"n":5, "dmg":-1, "s":5, "r":13, "des":"a-whiteDisp", "dest":8, \
"tr":{"n":2, "f":10, "c":(255, 255, 255), "o":255, "z":5, "d":1}, "spe":{}, "sound":"turretShoot4"}, \
\
"whiteBullet2":\
{"n":5, "dmg":-1, "s":7, "r":13, "des":"a-whiteDisp", "dest":6, \
"tr":None, "spe":{}, "sound":"shortShoot"}, \
\
"greenFollower":\
{"n":6, "dmg":-1, "s":8, "r":17, "des":"a-greenDes", "dest":12, \
"tr":{"n":3, "f":10, "c":(0, 255, 0), "o":150, "z":5, "d":1}, "spe":{"follow":{"f":7}}, "sound":"engShoot"}, \
\
"real_bullet":\
{"n":7, "dmg":-1, "s":30, "r":7, "des":"a-bulletDes", "dest":12, \
"tr":{"n":1, "f":10, "c":(20, 20, 20), "o":200, "z":1, "d":0}, "spe":{"doubleVerif":{}}, "sound":"bulletShoot"}, \
\
"ghostBullet":\
{"n":8, "dmg":-1, "s":8, "r":18, "des":None, "dest":0, \
"tr":{"n":3, "f":15, "c":(255, 150, 255), "o":255, "z":5, "d":1}, "spe":{"ghost":{}}, "sound":"engShoot"}, \
\
"bomb":\
{"n":9, "dmg":-1, "s":4, "r":21, "des":None, "dest":0, \
"tr":{"n":5, "f":10, "c":(25, 25, 25), "o":255, "z":6, "d":1}, "spe":{"explode":{"p":"whiteBullet2","nbFrag":12, "r":40, "dmg":20, "c":(255, 255, 255)}}, "sound":"turretShoot2"}, \
\
"greenBomb":\
{"n":15, "dmg":-1, "s":6, "r":21, "des":None, "dest":0, \
"tr":{"n":5, "f":10, "c":(25, 25, 25), "o":255, "z":6, "d":1}, "spe":{"explode":{"p":"greenArrow", "nbFrag":10, "r":40, "dmg":20, "c":(0, 255, 0)}}, "sound":"turretShoot2"}, \
\
"blueBullet":\
{"n":10, "dmg":-1, "s":12, "r":12, "des":"a-blueDestruction", "dest":14, \
"tr":{"n":4, "f":15, "c":(0, 100, 255), "o":255, "z":5, "d":0}, "spe":{}, "sound":"turretShoot1"}, \
\
"greenArrow":\
{"n":11, "dmg":-1, "s":10, "r":12, "des":"a-gArrDes", "dest":9, \
"tr":{"n":4, "f":15, "c":(0, 100, 0), "o":255, "z":2, "d":0}, "spe":{"disappear":{"life":35}}, "sound":"shortShoot"}, \
\
"bouncingArc":\
{"n":12, "dmg":-1, "s":6, "r":18, "des":"a-fireBallOff", "dest":18, \
"tr":{"n":4, "f":24, "c":(255, 200, 0), "o":200, "z":8, "d":1}, "spe":{"bounce":{"b":2}}, "sound":"engShoot"}, \
\
"redBoss":\
{"n":14, "dmg":-1, "s":4, "r":15, "des":None, "dest":0, \
"tr":{"n":6, "f":18, "c":(255, 0, 0), "o":200, "z":6, "d":1}, "spe":{"follow":{"f":5}, "explode":{"p":"redBullet", "nbFrag":14, "r":50, "dmg":40, "c":(255, 0, 0)}, "shooting":{"p":"redBullet", "cd":40, "nb":9}}, "sound":"bigShoot"}, \
\
}

proj_group = (
"redBullet",
"blueBullet",
"fireball",
"blueBullet",
"energyOrb",
"whiteBullet",
"greenFollower",
"real_bullet",
"ghostBullet",
"greenArrow",
"bomb",
"bouncingArc",
"redBoss",
"greenBomb",
)
