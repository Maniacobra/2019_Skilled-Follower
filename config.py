# -*- coding: utf-8 -*-

from pygame import Rect
from obj_models import map_object_models

interface_images = {

"bg":(
"interface/background",
"interface/gameBackground",
"interface/editor_grid"),
"scorebar":("interface/scorebar", ),
"symbols":(
"interface/fx",
"interface/music", ),
"statBar":(
"interface/statBar",
"interface/statTab", ),
"title":("interface/skilled_follower", ),
"tutorial":(
"interface/tuto1",
"interface/tuto2",
"interface/tuto3")
}

player_images = {

"player":(
"player/player_0",
"player/player_1",
"player/player_2",
"player/player_3",
"player/player_4",
"player/player_5",
"player/player_freeze",
"player/player_white", ),
"playerAttributes":("player/cursorCircle",
"player/shoot_direction",
"player/shield"),
}

game_objects_images = {

"start":("blocks/start", ),
"exit":"3:blocks/exit/exit",
"exit_close":("blocks/exit/exit_close", ),
"glassBlock":(
"blocks/glass",
"blocks/glass_small", ),
"spikes":("blocks/floor_spikes", ),
"round_spikes":("blocks/round_spikes", ),
"spike_square":(
"blocks/spikes",
"blocks/small_spikes", ),
"largeWall":(
"blocks/wall1_0",
"blocks/wall1_1",
"blocks/wall1_2",
"blocks/wall1_3", ),
"smallSquare":(
"blocks/square",
"blocks/small_square"),
"smallWall":(
"blocks/wall2_0",
"blocks/wall2_1",
"blocks/wall2_2",
"blocks/wall2_3", ),
"wood_block":(
"blocks/wood",
"blocks/small_wood", ),
"spiky_wood":("blocks/spiky_wood", ),
"spiky_wheel":("blocks/spiky_wheel", ),
"pylone":(
"blocks/pylone",
"blocks/cone",
"blocks/small_cone"),
"wood_cone":(
"blocks/w_cone0",
"blocks/w_cone1", ),
"glass_cone":(
"blocks/g_cone0",
"blocks/g_cone1", ),
"turret":(
"blocks/turret_red",
"blocks/turret_blue",
"blocks/turret_yellow",
"blocks/turret_green",
"blocks/turret_white",
"blocks/turret_sniper", ),
"laz_turret":(
"blocks/laz_turret_red",
"blocks/laz_turret_blue",
"blocks/laz_turret_green", ),
"laz_square":(
"blocks/lazer_square_red",
"blocks/lazer_square_blue",
"blocks/lazer_square_green", ),
"star":("blocks/energyGenerator", ),
"cannon":(
"attributes/cannon_red",
"attributes/cannon_blue",
"attributes/cannon_yellow",
"attributes/cannon_green",
"attributes/cannon_white",
"attributes/sniper", ),
"cannon_double":(
"attributes/cannon_red_double",
"attributes/cannon_blue_double",
"attributes/cannon_yellow_double",
"attributes/cannon_green_double",
"attributes/cannon_white_double", ),
"lazer":(
"attributes/lazer_red",
"attributes/lazer_blue",
"attributes/lazer_green", ),
"circularSaw":
("blocks/saw", ),
"square_button":(
"blocks/button_off",
"blocks/button_on", ),
"door":(
"blocks/door_close",
"blocks/door_open", ),
"param":("blocks/param", ),
"teleporter":("blocks/tp", ),
"tpCursor":("attributes/tpCursor", ),
"plTp":("attributes/plTp", ),
"small_magicWall":(
"blocks/magicWall0_off",
"blocks/magicWall0_on",
"blocks/magicWall0_open", ),
"med_magicWall":(
"blocks/magicWall1_off",
"blocks/magicWall1_on",
"blocks/magicWall1_open", ),
"large_magicWall":(
"blocks/magicWall2_off",
"blocks/magicWall2_on",
"blocks/magicWall2_open", ),
"screenBlock":("blocks/screenBlock", ),
"spike_wall":(
"blocks/spike_wall",
"blocks/small_spike_wall",
"blocks/spike_bar",
"blocks/spike", ),
"a-ring":"2:blocks/ring/ring",
"tesla":("blocks/tesla", ),
}

effects_animations = {

"a-miniExplosion":"2:animations/projDes/whArDes",
"a-star":"2:animations/projDes/blFragDes",
"a-redDestruction":"3:animations/projDes/rBullDes",
"a-fireBallOff":"3:animations/projDes/fbDes",
"a-electricity":"2:animations/projDes/enOrbDes",
"a-whiteDisp":"1:animations/projDes/wBullDes",
"a-greenDes":"1:animations/projDes/gFollDes",
"a-bulletDes":"1:animations/projDes/realBuDes",
"a-blueDestruction":"2:animations/projDes/bBullDes",
"a-gArrDes":"1:animations/projDes/gArrDes",
"a-playerDeath":"11:animations/playerDes/playerDes",
"a-door":"4:animations/door/door",
}

projectiles_images = {

"projectiles":(
"projectiles/whiteArrow",
"projectiles/blueFragment",
"projectiles/redBullet",
"projectiles/fireball",
"projectiles/energyOrb",
"projectiles/whiteBullet",
"projectiles/greenFollower",
"projectiles/bullet",
"projectiles/ghostBullet",
"projectiles/bomb",
"projectiles/blueBullet",
"projectiles/greenArrow",
"projectiles/bounce",
"projectiles/afterBounce",
"projectiles/red_boss",
"projectiles/greenBomb",
),

}

sounds_dict = {

"playerDeath":"death",
"blockDestruction":"destroy",
"projectileHit":"hit",
"shoot1":"left_shoot",
"shoot2":"right_shoot",
"turretShoot1":"shoot1",
"turretShoot2":"shoot2",
"bulletShoot":"shoot3",
"turretShoot4":"shoot4",
"bigShoot":"shoot6",
"shortShoot":"shoot5",
"engShoot":"dzioup",
"impulse":"impulse",
"bombExp1":"mini_impulse",
"win":"win",
"bip":"bip",
"click":"click",
"prevSignal":"prevent_signal",
"shieldLoss":"shield_loss",
"lazer":"lazer",
"door":"door",
"tpEnter":"tpEnter",
"tpExit":"tpExit",
"magicWall_close":"magicWall_close",
"magicWall_open":"magicWall_open",
"collect":"collect",
"electric_strike":"strike",
"exit_open":"exit_open",
"bounce":"bounce",
"projDes":"projectileDes",
"ding":"ding",
"button":"button",
"time":"time",

}

musics = {
"main_music":("musics/main_menu.wav", 1.75),
"victory_music":("musics/end_loop.wav", 1.0),
"game_musics":[
("musics/The beginning of a challenge.wav", 0.6),
("musics/Survive that.wav", 0.6),
("musics/A dream of success.wav", 2.8)]
}

fonts_dict = {

"simpleText":("consola.ttf", 15),
"impact":("impact.ttf", 20),
"mainFont":("Pixellari.ttf", 30),
"smallMainFont":("Pixellari.ttf", 23),
"digital":("digital-7.ttf", 30),
"title":("ka1.ttf", 65),
"buttons":("Square.ttf", 40),
"smallButtons":("Square.ttf", 30),

}

defaultMap = [
{"id":"start-12:12[0.0]" ,"name":"start", "rect":Rect(12, 12, 100, 100), "texture":0, "angle":0, "model":map_object_models["start"]},
{"id":"exit-1241:643[0.0]" ,"name":"exit", "rect":Rect(1241, 643, 110, 110), "texture":0, "angle":0, "model":map_object_models["exit"]},
{"id":"spikes-653:354[0.0]", "name":"spikes" ,"rect":Rect(653, 354, 80, 80), "texture":0, "angle":0, "model":map_object_models["spikes"]},
]

stats_default = {
"firstLauch":0,
"totalTime":0,
"totalScore":0,
"distanceTraveled":0,
"projShooted":0,
"blockDestroyed":0,
"totalDamages":0,
"shieldsDestroyed":0,
"gamesFailed":0,
"levelsCompleted":0,
"deaths":0,
"diff_s-easy":[0, 0],
"diff_easy":[0, 0, (0, 3600), (0, 3600), 0],
"diff_normal":[0, 0, (0, 3600), (0, 3600), 0],
"diff_hard":[0, 0, (0, 3600), (0, 3600), 0],
"diff_challenge":[0, 0, (0, 3600), (0, 3600), 0],
"diff_s-challenge":[0, 0, (0, 3600), (0, 3600), 0],
"discovered_levels":[],
"completed_levels":[],
}

div_paths = {"sett":"settings.txt", "lang":"langages.txt", "stats":"stats"}

urls = {
"web":"http://maniacobra.com/"
}

mail = "maniacobra@orange.fr"
