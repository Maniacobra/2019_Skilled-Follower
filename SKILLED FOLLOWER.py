# -*- coding: utf-8 -*-

import sys
Log = open("log.txt", "w")
sys.stderr = Log
sys.stdout = Log

print("[CHARGEMENT] Importations des modules")

from os import listdir, chdir
chdir("ressources/")

import pygame
from pygame.locals import *
from time import time, sleep
import cProfile
import pstats
import pickle
import random
import os

print("[CHARGEMENT] Importations des fichiers")

import game_values as GAMEVALUES
from config import *
from mainMenu import MainMenu, TutoMenu
from settMenu import SettingsMenu
from statsMenu import StatsMenu
from game import Game
from victory_screen import VictoryScreen
from config import defaultMap
from map_object import map_object
from fct import *
from visuals import flash, animated_bg
import res

print("[CHARGEMENT] Initialisation de la fenêtre")

res.load_infos()

pygame.display.set_icon(pygame.image.load("icon.png"))

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

window = pygame.display.set_mode(GAMEVALUES.defaultWinSize)
res.display_win_update()

res.load_fonts()

window.fill((0, 0, 0))
window.blit(res.fonts["mainFont"].render("{} 20%".format(res.language["loading"]), 1, (255,255,255)), (0, 0))
pygame.display.flip()

pygame.display.set_caption("Skilled Follower {}".format(GAMEVALUES.version))

if pygame.display.get_surface().get_size() == GAMEVALUES.defaultWinSize:
	windowL = window
	print("[INFO] Programmes de redimension de la fenetre desactives")
else:
	windowL = pygame.Surface(GAMEVALUES.defaultWinSize)
	print("[INFO] Programmes de redimension de la fenetre actives")

os.environ['SDL_VIDEO_CENTERED'] = '1'

print("[CHARGEMENT] Chargement des donnees")

window.blit(res.fonts["mainFont"].render("{} 21% (images)".format(res.language["loading"]), 1, (255,255,255)), (0, 0))
pygame.display.flip()

res.load_images()

window.fill((0, 0, 0))
window.blit(res.fonts["mainFont"].render("{} 65% (medias)".format(res.language["loading"]), 1, (255,255,255)), (0, 0))
pygame.display.flip()

res.create_soundMananger()

print("[CHARGEMENT] Lancement du jeu")

window.fill((0, 0, 0))
window.blit(res.fonts["mainFont"].render("{} 90% (launch)".format(res.language["loading"]), 1, (255,255,255)), (0, 0))
pygame.display.flip()

def test(game, window, frames):

	progress = 0
	for i in range(0, frames):
		progress += 100/frames
		chargebar = pygame.Rect(585, 394, progress*2, 20)
		game.update()
		game.show(window)
		p_text = res.fonts["impact"].render("Profiling {}%".format(progress.__round__()), 1, (255, 255, 255))
		window.blit(p_text, p_text.get_rect(center=(683, 374)))
		pygame.draw.rect(window, (100, 100, 100), (585, 394, 200, 20))
		pygame.draw.rect(window, (255, 255, 255), chargebar)
		if game.redirect is not None:
			break
		pygame.display.flip()

def loadLevel(name, Map, scoreMlt):

	if not name in res.stats["discovered_levels"] and name is not None:
		res.stats["discovered_levels"].append(name)
	Level = {"pos":[(0, 0), (0, 0)], "obj":pygame.sprite.Group()}
	Map.append({"id":"TOPBORDER", "name":None, "rect":pygame.Rect(0, 0, 1366, 10), "texture":0, "angle":0, "model":map_object_models["blackBlock"]})
	Map.append({"id":"LEFTBORDER", "name":None, "rect":pygame.Rect(0, 0, 10, 758), "texture":0, "angle":0, "model":map_object_models["blackBlock"]})
	Map.append({"id":"BOTTOMBORDER", "name":None, "rect":pygame.Rect(0, 758, 1366, 10), "texture":0, "angle":0, "model":map_object_models["blackBlock"]})
	Map.append({"id":"RIGHTBORDER", "name":None, "rect":pygame.Rect(1356, 0, 10, 768), "texture":0, "angle":0, "model":map_object_models["blackBlock"]})
	for obj in Map:
		if obj["name"] == "start":
			Level["pos"][0] = obj["rect"].center
		elif obj["name"] == "exit":
			Level["pos"][1] = obj["rect"].center
		sprite = map_object(obj["id"], obj["name"], obj["rect"], obj["texture"], obj["angle"], obj["model"], scoreMlt)
		Level["obj"].add(sprite)

	return Level, name

def loadTrack():

	levelTrack = []
	for folderName in range(1, GAMEVALUES.level_nb+1):
		fileName = "DEFAULT_LEVEL_ERROR"
		selected = "DEFAULT_LEVEL_ERROR"
		availabe_levels = []
		Level = defaultMap
		try:
			availabe_levels = listdir("levels/{}".format(folderName))
			for mapFile in availabe_levels:
				if len(mapFile.split(".")) < 2 or not mapFile.split(".")[-1] == "sf":
					availabe_levels.remove(mapFile)
			if len(availabe_levels) == 0:
				raise IOError
			selected = random.choice(availabe_levels)
			fileName = "levels/{}/{}".format(folderName, selected)
			with open(fileName, "rb") as lvlFile:
				Level = pickle.Unpickler(lvlFile).load()
		except IOError:
			print("[ERREUR] Le dossier {} est vide ou n'existe pas".format(folderName))
		except:
			print("[ERREUR] Echec du chargement du niveau {} suite à une erreur inconnue".format(folderName))
		levelTrack.append((fileName, Level))
		print("[INFO] Niveau {} : Sur {} fichier(s),  '{}' charge".format(folderName, len(availabe_levels), selected))
	return levelTrack

def loadPack(folderName, shuff=False):

	levelTrack = []
	availabe_levels = []
	try:
		availabe_levels = listdir("levels/packs/{}")
		if len(availabe_levels) == 0:
			raise IOError
		for fileName in availabe_levels:
			with open("levels/pack/{}/{}".format(folderName, fileName), "rb") as lvlFile:
				levelTrack.append(pickle.Unpickler(lvlFile).load())
		if shuff:
			availabe_levels = random.shuffle(availabe_levels)
	except IOError:
		print("[ERREUR] Le dossier {} est vide ou n'existe pas".format(folderName))
	except:
		print("[ERREUR] Echec du chargement du pack {} suite à une erreur inconnue".format(folderName))
	return levelTrack

windowSize = windowL.get_size()

profile = cProfile.Profile()
clock = pygame.time.Clock()

if res.stats["firstLauch"] == 0:
	res.stats["firstLauch"] = int(time())
mainMenu = MainMenu(clock)
settMenu = SettingsMenu()
statsMenu = StatsMenu()
tutoMenu = TutoMenu()
victoryMenu = None
actualMenu = "main"
animBg = animated_bg()

game = None
levelTimes = []

dispNow = True

res.soundMananger.playMusic(1)

print("[LOG] Chargement termine.")

################################################################################ DEMARRAGE DE LA BOUCLE PRINCIPALE

while actualMenu != "q":

	res.soundMananger.update()

	if windowSize != pygame.display.get_surface().get_size():
		print("[INFO] Reinitialisation du calque de la fenetre : {}".format(pygame.display.get_surface().get_size()))
		if pygame.display.get_surface().get_size() == GAMEVALUES.defaultWinSize:
			windowL = window
			print("[INFO] Programmes de redimension de la fenetre desactives")
		else:
			windowL = pygame.Surface(GAMEVALUES.defaultWinSize)
			print("[INFO] Programmes de redimension de la fenetre actives")
	windowSize = pygame.display.get_surface().get_size()

	clock.tick(60)

	if actualMenu == "main": ################################################### BOUCLE MAIN

		if mainMenu.redirect is None:
			mainMenu.update(animBg)
			if dispNow:
				mainMenu.show(windowL, animBg)
		else:
			actualMenu = mainMenu.redirect
			if actualMenu == "stats":
				statsMenu = StatsMenu()
			elif actualMenu == "tuto_launch":
				tutoMenu = TutoMenu(True)
				actualMenu = "tuto"
			mainMenu.reinit()

	elif actualMenu == "sett": ################################################# PREFERENCES

		if settMenu.redirect is None:
			settMenu.update(animBg)
			if dispNow:
				settMenu.show(windowL, animBg)
		else:
			actualMenu = settMenu.redirect
			mainMenu.reinit()
			settMenu.reinit()

	elif actualMenu == "tuto": ################################################# TUTO

		if tutoMenu.redirect is None:
			tutoMenu.update()
			if dispNow:
				tutoMenu.show(windowL)
		else:
			actualMenu = tutoMenu.redirect
			mainMenu.reinit()
			tutoMenu.redirect = None
			tutoMenu.slide = 0
			tutoMenu.dedis = None

	elif actualMenu == "stats": ################################################ STATS

		if statsMenu.redirect is None:
			statsMenu.update(animBg)
			if dispNow:
				statsMenu.show(windowL, animBg)
		else:
			actualMenu = statsMenu.redirect
			mainMenu.reinit()

	elif actualMenu == "launchGame": ########################################### LAUNCHGAME

		levelTimes = []
		print("[LOG] Lancement d'une partie")
		res.soundMananger.playMusic()
		levels = loadTrack()
		stage = 1
		if game is not None:
			game = Game(mainMenu.diffNb, *loadLevel(*levels[0], mainMenu.gameLaunchArgs[1]), 1, clock, 1, *mainMenu.gameLaunchArgs)
		else:
			game = Game(mainMenu.diffNb, *loadLevel(*levels[0], mainMenu.gameLaunchArgs[1]), 1, clock, 0, *mainMenu.gameLaunchArgs)
		gameScore = game.A_G_V.score

		res.stats[res.get_diff(mainMenu.diffNb)][0] += 1

		actualMenu = "game"

	elif actualMenu == "launchTest": ########################################### LAUNCHTEST

		levelTimes = []
		print("[LOG] Lancement de test de niveau")
		res.soundMananger.stopMusic()
		try:
			with open(res.settings["DEFAULT_FILE"], "rb") as lvlFile:
				level = pickle.Unpickler(lvlFile).load()
			stage = 0
			g_fade = 1
			if game is not None and game.A_G_V.end == "next":
				g_fade = 0
			print(level)
			game = Game(mainMenu.diffNb, *loadLevel(None, level, mainMenu.gameLaunchArgs[1]), 0, clock, g_fade, True, 1, -1)
			gameScore = game.A_G_V.score
			actualMenu = "game"
		except IOError:
			actualMenu = "endGame"
			print("[ERREUR] Test de niveau : Fichier '{}' non trouve".format(res.settings["DEFAULT_FILE"]))

	elif actualMenu == "endGame": ############################################## ENDGAME

		print("[LOG] Arret de la partie")
		res.soundMananger.stopAll()
		res.soundMananger.playMusic(1)
		actualMenu = "main"
		mainMenu.reinit()
		mainMenu.transition.add(flash((0, 0, 0), 255, 30))
		game = None

	elif actualMenu == "game": ################################################# BOUCLE GAME

		if game.redirect is None:
			if game.profile:
				game.profile = False
				profile.run("test(game, windowL, int(GAMEVALUES.profileFrames))")
				stats = pstats.Stats(profile).sort_stats("cumtime",  "time")
				print("[PROFILING]\n     ---------------  PROFILING ({} frames)  ---------------    \n".format(int(GAMEVALUES.profileFrames)))
				stats.print_stats()
			else:
				game.update()
				if dispNow:
					game.show(windowL)
		elif game.redirect == "next":
			if not game.mapName in res.stats["completed_levels"] and game.mapName is not None:
				res.stats["completed_levels"].append(game.mapName)
			res.saveStats()
			if stage > 0:
				statTarget = res.get_diff(mainMenu.diffNb)
				if stage+1 > GAMEVALUES.level_nb:
					if mainMenu.diffNb != 5:
						res.stats[statTarget][4] = GAMEVALUES.level_nb
						actualMenu = "winGame"
					else:
						actualMenu = "endGame"
					print("[LOG] Succes de la partie")
				else:
					if mainMenu.diffNb != 5:
						if res.stats[statTarget][4] < stage:
							res.stats[statTarget][4] = stage
					game = Game(mainMenu.diffNb, *loadLevel(*levels[stage], mainMenu.gameLaunchArgs[1]), stage+1, clock, 0, mainMenu.gameLaunchArgs[0], mainMenu.gameLaunchArgs[1], game.A_G_V.lifes, game.A_G_V.score, game.chrono)
					gameScore = game.A_G_V.score
				levelTimes.append(game.chrono)
				stage += 1
			else:
				actualMenu = "launchTest"
		elif game.redirect == "leave":
			actualMenu = "endGame"
		elif game.redirect == "loose":
			print("[LOG] Echec")
			if game.A_G_V.lifes < 0:
				if stage > 0:
					actualMenu = "launchGame"
					print("[LOG] Recommencement")
				else:
					print("[RESULTATS] : {} pts en {} sec".format(game.A_G_V.score.__round__(2), game.chrono.__round__(2)))
					actualMenu = "launchTest"
			else:
				if stage > 0:
					if stage == 1:
						game = Game(mainMenu.diffNb, *loadLevel(*levels[stage-1], mainMenu.gameLaunchArgs[1]), stage, clock, 1, *mainMenu.gameLaunchArgs)
					else:
						if gameScore >= 60:
							game.A_G_V.score = gameScore+GAMEVALUES.loosePts
						else:
							game.A_G_V.score = 30
						game = Game(mainMenu.diffNb, *loadLevel(*levels[stage-1], mainMenu.gameLaunchArgs[1]), stage, clock, 1, mainMenu.gameLaunchArgs[0], mainMenu.gameLaunchArgs[1], game.A_G_V.lifes, game.A_G_V.score, game.chrono)
				else:
					actualMenu = "launchTest"
		elif game.redirect == "pause":
			print("[LOG] Pause")
			actualMenu = "pause"
		elif game.redirect == "quit":
			actualMenu = "q"

	elif actualMenu == "pause": ################################################ BOUCLE PAUSE

		if game.pauseMenu.redirect is None:
			game.pauseMenu.update()
			if dispNow:
				game.show(windowL)
				game.pauseMenu.show(windowL)
		elif game.pauseMenu.redirect == "leave":
			actualMenu = "endGame"
		elif game.pauseMenu.redirect == "continue":
			print("[LOG] Unpause")
			actualMenu = "game"
			game.eventUpdate()
			game.redirect = None
			game.pauseMenu.redirect = None
		elif game.pauseMenu.redirect == "quit":
			actualMenu = "q"
		elif game.pauseMenu.redirect == "restart":
			print("[LOG] Recommencement")
			if stage > 0:
				game = None
				actualMenu = "launchGame"
			else:
				actualMenu = "launchTest"
		elif game.pauseMenu.redirect == "pauseSett":
			actualMenu = "pauseSett"

	elif actualMenu == "pauseSett": ########################################### PAUSE SETT

		if settMenu.redirect is None:
			settMenu.update()
			if dispNow:
				game.show(windowL)
				settMenu.show(windowL)
		else:
			game.pauseMenu.reinit()
			if settMenu.redirect == "main":
				actualMenu = "pause"
			else:
				actualMenu = settMenu.redirect
			settMenu.reinit()

	elif actualMenu == "changeGraph": ########################################## CHANGE GRAPHS

		game.particles.reset(res.settings["MAX_PARTICLES"], res.settings["PARTICLES_FRAMES_UPDATE"])
		actualMenu = "pauseSett"
		settMenu.redirect = None
		print("[LOG] Graphiques reset")

	elif actualMenu == "winGame": ############################################## WINGAME

		statTarget = res.get_diff(mainMenu.diffNb)
		if statTarget != "diff_s-easy":
			res.stats[statTarget][1] += 1
			if game.A_G_V.score > res.stats[statTarget][2][0]:
				res.stats[statTarget][2] = int(game.A_G_V.score), game.chrono.__round__(2)
			if game.chrono < res.stats[statTarget][3][1] or res.stats[statTarget][3][1] == 0:
				res.stats[statTarget][3] = int(game.A_G_V.score), game.chrono.__round__(2)
		victoryMenu = VictoryScreen(game.A_G_V.score, levelTimes, mainMenu.diffNb)
		res.soundMananger.stopAll()
		actualMenu = "victory"

	elif actualMenu == "victory": ############################################## VICTORYSCREEN

		victoryMenu.update()
		if dispNow:
			victoryMenu.show(windowL)
		if victoryMenu.redirect is not None:
			actualMenu = victoryMenu.redirect

	if pygame.display.get_surface().get_size() != GAMEVALUES.defaultWinSize:
		window.blit(pygame.transform.scale(windowL, pygame.display.get_surface().get_size()), (0, 0))

	pygame.display.flip()

	if res.settings["FPS_ADAPTATION"] == "30" or (res.settings["FPS_ADAPTATION"] == "AUTO" and clock.get_fps() < 50):
		if res.settings["FPS_ADAPTATION"] == "AUTO":
			res.FPS = 30
		if dispNow:
			dispNow = False
		else:
			dispNow = True
	else:
		res.FPS = 60
		if not dispNow:
			dispNow = True

print("[LOG] Sauvegarde des stats")
res.saveStats()

print("[LOG] Fermeture du jeu")

sleep(0.25)
pygame.quit()
