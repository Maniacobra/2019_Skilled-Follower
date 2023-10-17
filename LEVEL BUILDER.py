# -*- coding: utf-8 -*-

import sys
Log = open("log.txt", "w")
sys.stderr = Log

from os import listdir, chdir
chdir("ressources/")

import pickle
import pygame
from pygame.locals import *
from time import sleep
from copy import deepcopy
from math import radians, pi, degrees
import random
import os

import game_values as GAMEVALUES
from config import defaultMap
from obj_models import map_object_models
from map_object import map_object
from fct import *
from command_interpreter import enter_command
import res

editing_map = input("Fichier :")
if editing_map == "":
	with open("settings.txt", "r") as settFile:
		sett = ""
		for line in settFile.read().split("\n"):
			if line.split(":")[0] == "DEFAULT_FILE":
				editing_map = line.split(":")[1][:-2]
	print("Ouverture de {}".format(editing_map))
else:
	editing_map = "{}.sf".format(editing_map)

total_nb_levels = 0
for i in range(1, GAMEVALUES.level_nb+1):
	for file in os.listdir("levels/{}".format(i)):
		if file[-3:] == ".sf":
			total_nb_levels += 1
			print(file)
			if file == editing_map:
				editing_map = "levels/{}/{}".format(i, editing_map)
				print("{} trouvé au dossier {}".format(editing_map, i))
print("\nNombre total de niveaux : {}/{} ({}%)\n".format(total_nb_levels, GAMEVALUES.totalLevels, (total_nb_levels/GAMEVALUES.totalLevels).__round__(3)*100))

try:
	with open(editing_map, "rb") as lvlFile:
		Level = pickle.Unpickler(lvlFile).load()
except IOError:
	print("{} non trouvé".format(editing_map))
	Level = defaultMap

pygame.display.set_icon(pygame.image.load("icon.png"))

pygame.init()

window = pygame.display.set_mode((1366, 768))
pygame.display.set_caption("SF Level Editor")

pygame.key.set_repeat(500,25)

res.load_fonts()
res.load_images("interface", "objects")

gridSize = 5
stop = False
mousePos = 0, 0
place = 0, 0
text1_changed = 0
text2_changed = 0
obj_info_txt_changed = 0
waitFrames = 0
blinking_rect = 0

availabe_objects = {
"essentials":["start", "exit", "ring", "blackBlock"],
"solids":["largeWall", "smallWall", "smallSquare", "pylone"],
"destroyables":["wood_block", "glassBlock", "wood_cone", "glass_cone"],
"hazards":["spikes", "round_spikes", "spike_square", "spike_wall", "saw", "spiky_wood", "spiky_wheel"],
"turrets":["standartTurret", "blueTurret", "softTurret", "multipleShootTurret", "techTurret", "sniperTurret", "sequenceTurret", "arrowTurret", "g-follTurret", "duoTurret", "ghostTurret", "bombTurret"],
"powers":["star", "lazerTurret", "lazerCube", "teslaTurret"],
"mechanics":["contact_button", "door", "invisible_element", "screenBlock"],
"specials":["teleporter", "small_magicWall", "med_magicWall", "large_magicWall"],
}

actualObjGroup = "essentials"

textureObjectsKeys = {K_1:0, K_2:1, K_3:2, K_4:3, K_5:4, K_6:5, K_7:6, K_8:7, K_9:8, K_0:9}

def changeObject(name):

	global obj_info_txt_changed
	global toolmode
	global objName
	global model
	global usedObject
	global previousUsedObject
	global actualObjGroup
	objName = name
	obj_info_txt_changed = 120
	toolmode = False
	model = map_object_models[objName]
	if model["name"] is not None:
		rect = res.images[model["name"]][0].get_rect(center=place)
	else:
		rect = pygame.Rect(0, 0, 100, 100)
		rect.center = place
	if usedObject == {}:
		previousUsedObject = {"name":objName, "rect":rect, \
		"texture":0, "angle":0, "model":model}
	else:
		previousUsedObject = usedObject
	usedObject = {"name":objName, "rect":rect, \
	"texture":0, "angle":0, "model":model}
	for groupName, group in availabe_objects.items():
		if name in group:
			actualObjGroup = groupName

text_reinit = res.fonts["mainFont"].render("Niveau réinitialisé", 1, (255, 255, 255))
text_exit = res.fonts["mainFont"].render("Niveau enregistré avec succès", 1, (255, 255, 255))
text_cmd = res.fonts["mainFont"].render("Entrez une ou plusieurs commandes dans la console", 1, (255, 255, 255))

usedObject = {}
actualObject = 0
previousUsedObject = {}
selectedObjIndex = None
savedIds = []
savedCoords = []
changeObject("start")
attr_get_rect = lambda object: pygame.transform.rotate(res.images[object["model"]["name"]][object["texture"]], orth_angle(object["angle"])).get_rect(center=object["rect"].center)
objName = "start"
toolmode = True

while stop == False:

	pygame.time.Clock().tick(60)

	for event in pygame.event.get():

		if event.type == QUIT: ################################################# QUIT
			stop = True

		elif event.type == KEYDOWN: ############################################ TOUCHE

			if event.key == K_RETURN:

				with open(editing_map, "wb") as lvlFile:
					lvlFile = pickle.Pickler(lvlFile)
					lvlFile.dump(Level)
				with open("settings.txt", "r") as settFile:
					sett = ""
					for line in settFile.read().split("\n"):
						if line.split(":")[0] == "DEFAULT_FILE":
							line = "DEFAULT_FILE:{}_s".format(editing_map)
						if line != "!":
							line += "\n"
						sett += line
				with open("settings.txt", "w") as lvlFile:
					lvlFile.write(sett)
				window.fill((0, 0, 0),text_exit.get_rect(center=(683, 384)).inflate(25, 10))
				window.blit(text_exit, text_exit.get_rect(center=(683, 384)))
				pygame.display.flip()
				sleep(1.0)

			elif event.key == K_TAB:

				if toolmode == True:
					toolmode = False
				else:
					toolmode = True

			if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):

				if event.key == K_UP:
					rot = radians(5)
				elif event.key == K_DOWN:
					rot = radians(-5)
				elif event.key == K_LEFT:
					rot = pi/2
				else:
					rot = -pi/2
				selected = None
				if toolmode:
					if selectedObjIndex is not None:
						selected = Level[selectedObjIndex]
				else:
					selected = usedObject
				if selected is not None:
					selected["angle"] = degrees((radians(selected["angle"])+rot)%(pi*2))
					if selected["model"]["name"] is not None:
						selected["rect"] = attr_get_rect(selected)

			elif event.key == K_q:
				changeObject("start")
			elif event.key == K_w:
				changeObject("largeWall")
			elif event.key == K_e:
				changeObject("wood_block")
			elif event.key == K_r:
				changeObject("spikes")
			elif event.key == K_t:
				changeObject("standartTurret")
			elif event.key == K_y:
				changeObject("star")
			elif event.key == K_u:
				changeObject("contact_button")
			elif event.key == K_i:
				changeObject("teleporter")

			elif event.key in textureObjectsKeys.keys():
				obj_info_txt_changed = 30
				selected = None
				if toolmode:
					if selectedObjIndex is not None:
						selected = Level[selectedObjIndex]
				else:
					selected = usedObject
				if selected is not None and selected["model"]["name"] is not None:
					if textureObjectsKeys[event.key] >= len(res.images[selected["model"]["name"]]):
						selected["texture"] = len(res.images[selected["model"]["name"]])-1
					else:
						selected["texture"] = textureObjectsKeys[event.key]
					selected["rect"] = attr_get_rect(selected)

			elif event.key == K_BACKSPACE:
				savedIds = []
				savedCoords = []
				Level = list(defaultMap)
				text2_changed = 60

			elif event.key == K_LALT or event.key == K_RALT:
				usedObject, previousUsedObject = previousUsedObject, usedObject
				usedObject["rect"].center = previousUsedObject["rect"].center

			elif event.key == K_LCTRL:
				text1_changed = 30
				if gridSize == 5:
					gridSize = 10
				elif gridSize == 10:
					gridSize = 1
				elif gridSize == 1:
					gridSize = 2
				elif gridSize == 2:
					gridSize = 5

			elif event.key == K_SPACE: ######################################### COMMANDES

				window.fill((0, 0, 0),text_cmd.get_rect(center=(683, 384)).inflate(25, 10))
				window.blit(text_cmd, text_cmd.get_rect(center=(683, 384)))
				pygame.display.flip()
				if toolmode == False:
					selected = usedObject
					print(selected)
					command = input("\nModifier les attributs de l'objet utilisé ({}) :\n-> ".format(selected["name"]))
				else:
					selected = None
					if selectedObjIndex is not None:
						selected = Level[selectedObjIndex]
						print(selected)
						command = input("\nModifier les attributs de l'objet pointé ({}) :\n-> ".format(selected["name"]))
				if selected is not None:
					text1_changed = 0
					text2_changed = 0
					obj_info_txt_changed = 30
					modifs = 0
					if command != "":
						obj, success = enter_command(selected, command, savedIds, savedCoords)
						if success:
							modifs += 1
						selected = obj
					while command != "":
						if toolmode:
							Level[id] = obj
						else:
							usedObject = obj
						command = input("-> ")
						if command != "":
							obj, success = enter_command(selected, command, savedIds, savedCoords)
							if success:
								modifs += 1
						selected = obj
					if modifs == 0:
						print("\nAucune modification apportée")
					else:
						print("\n{} Modifications apportés à {}".format(modifs, selected["name"]))
					print("\n\n")

			elif event.key == K_F1 and selectedObjIndex is not None:

				savedIds.append(Level[selectedObjIndex]["id"])

			elif event.key == K_F2:

				savedIds = []

			elif event.key == K_F3:

				savedCoords.append(usedObject["rect"].center)

			elif event.key == K_F4:

				savedCoords = []

			elif event.key == K_F5 and selectedObjIndex is not None:

				objToReplace = Level[selectedObjIndex]
				Level.remove(objToReplace)
				Level.insert(0, objToReplace)

			elif event.key == K_F6 and selectedObjIndex is not None:

				objToReplace = Level[selectedObjIndex]
				Level.remove(objToReplace)
				Level.append(objToReplace)
                                
		elif event.type == MOUSEMOTION: ######################################## MOUSEMOTION

			mousePos = event.pos
			place = (int(mousePos[0]/gridSize)*gridSize+gridSize/2, int(mousePos[1]/gridSize)*gridSize+gridSize/2)
			usedObject["rect"].center = place

		if event.type == MOUSEBUTTONDOWN: ###################################### BOUTON

			if toolmode and selectedObjIndex is not None:

				if event.button == 1:
					toolmode = False
					usedObject = deepcopy(Level[selectedObjIndex])
					if not pygame.key.get_pressed()[K_LSHIFT]:
						del Level[selectedObjIndex]
				elif event.button == 3 and Level[selectedObjIndex]["model"]["name"] not in ("start", "exit"):
					del Level[selectedObjIndex]

			elif toolmode == False and event.button == 1:

				if usedObject["name"] == "start":
					for obj in enumerate(Level):
						if obj[1]["name"] == "start":
							del Level[obj[0]]
				elif usedObject["name"] == "exit":
					for obj in enumerate(Level):
						if obj[1]["name"] == "exit":
							del Level[obj[0]]
				newObj = deepcopy(usedObject)
				newObj["id"] = "{}-{}:{}[{}]".format(newObj["name"], newObj["rect"].x, newObj["rect"].y, random.random())
				Level.append(newObj)

			elif event.button == 5 and toolmode == False:
				actualObject += 1
				if actualObject >= len(availabe_objects[actualObjGroup]):
					actualObject = 0
				changeObject(availabe_objects[actualObjGroup][actualObject])

			elif event.button == 4 and toolmode == False:
				actualObject -= 1
				if actualObject < 0:
					actualObject = len(availabe_objects[actualObjGroup])-1
				changeObject(availabe_objects[actualObjGroup][actualObject])

	############################################################################ AFFICHAGE

	if toolmode:
		idList = []
		for id, obj in enumerate(Level):
			if obj["rect"].collidepoint(place):
				idList.append(id)
		for id in idList:
			selectedObjIndex = sorted(idList,key=lambda rect:(Level[rect]["rect"].width+Level[rect]["rect"].height)/2)[0]
		if len(idList) == 0:
			selectedObjIndex = None

	window.blit(res.images["bg"][-1], (0, 0))
	for obj in Level:
		if obj["model"]["name"] is not None:
			img = pygame.transform.rotate(res.images[obj["model"]["name"]][obj["texture"]], orth_angle(obj["angle"]))
			window.blit(img, obj["rect"])
		elif "colorShape" in obj["model"]["spe"]:
			param = obj["model"]["spe"]["colorShape"]
			pygame.draw.rect(window, (param["r"], param["v"], param["b"]), obj["rect"])
		elif obj["name"] == "invisible_element":
			window.blit(res.images["param"][0], obj["rect"])

	mix = []
	for obj in Level:
		mix.append(obj)
	if toolmode == False:
		mix.append(usedObject)
	for obj in mix:
		for spename, speval in obj["model"]["spe"].items():
			if spename in ("shooting", "multipleShooting", "randShoot", "seqShoot", "lazer"):
				if speval["r"] < 360:
					vect = get_vect(obj["angle"]+speval["r"]/2, 600)
					endpos = obj["rect"].centerx+vect[0], obj["rect"].centery+vect[1]
					pygame.draw.line(window, (255, 100, 255), obj["rect"].center, endpos)
					vect = get_vect(obj["angle"]-speval["r"]/2, 600)
					endpos = obj["rect"].centerx+vect[0], obj["rect"].centery+vect[1]
					pygame.draw.line(window, (255, 100, 255), obj["rect"].center, endpos)
			elif spename == "tesla":
				pygame.draw.circle(window, (255, 100, 100), obj["rect"].center, speval["scope"], 1)

	if toolmode == False:
		if obj["model"]["name"] is not None:
			img = pygame.transform.rotate(res.images[usedObject["model"]["name"]][usedObject["texture"]], orth_angle(usedObject["angle"]))
			window.blit(img, usedObject["rect"])
		if blinking_rect <= 30:
			color = (255, 255, 255)
			blinking_rect += 1
		elif blinking_rect >= 60:
			color = (255, 255, 255)
			blinking_rect = 0
		else:
			color = (255, 0, 0)
			blinking_rect += 1
		pygame.draw.rect(window,color, usedObject["rect"],1)
		arrow = get_vect(usedObject["angle"], (usedObject["rect"].width+usedObject["rect"].height)/2)
		center = usedObject["rect"].center
		pygame.draw.line(window, (100,200,200), center, (center[0]+arrow[0], center[1]+arrow[1]), 2)
		if obj_info_txt_changed > 0:
			obj_info_txt_changed -= 1
			if usedObject["model"]["h"] == -1:
				hp_txt = "Unbreakable"
			else:
				hp_txt = str(usedObject["model"]["h"])+"HP"
			if obj["model"]["name"] is None:
				st_str = "{} (No texture) {}".format(objName, hp_txt)
			else:
				st_str = "{} ({}/{}) {}".format(objName, usedObject["texture"]+1, len(res.images[usedObject["model"]["name"]]), hp_txt)
			subtitle = res.fonts["impact"].render(st_str, 1, (220, 220, 220))
			window.blit(subtitle, subtitle.get_rect(centerx=usedObject["rect"].centerx+10, y=usedObject["rect"].y+usedObject["rect"].height))
	else:
		obj_info_txt_changed = 0
		color = (0, 255, 0)
		if selectedObjIndex is not None:
			arrow = get_vect(Level[selectedObjIndex]["angle"], (Level[selectedObjIndex]["rect"].width+Level[selectedObjIndex]["rect"].height)/2)
			center = Level[selectedObjIndex]["rect"].center
			pygame.draw.rect(window, (150,150,255), Level[selectedObjIndex]["rect"], 4)
			pygame.draw.line(window, (100,200,200), center, (center[0]+arrow[0], center[1]+arrow[1]), 2)
			color = (0, 100, 255)
		pygame.draw.line(window, color, (place[0]-8, place[1]), (place[0]+8, place[1]))
		pygame.draw.line(window, color, (place[0], place[1]-8), (place[0], place[1]+8))
	text_liveCoord = res.fonts["simpleText"].render(str(place), 1, (255, 255, 255))
	window.blit(text_liveCoord, text_liveCoord.get_rect(topright=(1366, 0)))
	if text1_changed > 0:
		text_gridSize = res.fonts["simpleText"].render("Précision : {}px".format(gridSize),1,(255,255,255))
		window.blit(text_gridSize, (0, 0))
		text1_changed -= 1
	if text2_changed > 0:
		window.fill((0, 0, 0),text_reinit.get_rect(center=(683, 384)).inflate(25, 10))
		window.blit(text_reinit, text_reinit.get_rect(center=(683, 384)))
		text2_changed -= 1
	for text_line in lineTexts("!".join(savedIds), 0, "simpleText", [0, 750], -12):
		window.blit(text_line[0], text_line[1])
	for text_line in lineTexts("!".join([str(tupl) for tupl in savedCoords]), 1, "simpleText", [1366, 750], -12):
		window.blit(text_line[0], text_line[1])
	pygame.display.flip()
