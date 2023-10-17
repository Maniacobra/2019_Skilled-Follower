# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import choice
from time import time
from ctypes import windll
import pickle
import webbrowser

import game_values as GAMEVALUES
import config

images = None
fonts = None
settings = None
language = None
soundMananger = None
stats = None
FPS = 60
mail = config.mail
firstLaunch = False

def load_images(*categories):

	global images
	images = {}

	imgToLoad = []

	if "interface" in categories:
		imgToLoad.append(config.interface_images)
	if "objects" in categories:
		imgToLoad.append(config.game_objects_images)
	if "player" in categories:
		imgToLoad.append(config.player_images)
	if "proj" in categories:
		imgToLoad.append(config.projectiles_images)
	if "effects" in categories:
		imgToLoad.append(config.effects_animations)
	else:
		imgToLoad.append(config.interface_images)
		imgToLoad.append(config.game_objects_images)
		imgToLoad.append(config.player_images)
		imgToLoad.append(config.projectiles_images)
		imgToLoad.append(config.effects_animations)

	for imageGroup in imgToLoad:
		for group, paths in imageGroup.items():
			if type(paths) == str:
				pathsList = []
				imgs_len, origin_path = paths.split(":")
				for nb_img in range(int(imgs_len)+1):
					pathsList.append("{}_p{}".format(origin_path, nb_img))
				paths = pathsList
			images[group] = []
			for path in paths:
				if group == "tutorial":
					if settings is not None and settings["LANGUAGE"] == "FR":
						path += "_fr"
					else:
						path += "_en"
				images[group].append(pygame.image.load("images/{}.png".format(path)).convert_alpha())

def load_fonts():

	global fonts
	fonts = {}

	for name, font in config.fonts_dict.items():
		font = pygame.font.Font("fonts/{}".format(font[0]), font[1])
		fonts[name] = font

def load_infos():

	global settings
	global language
	global stats
	global FPS
	global firstLaunch
	settings = {}
	langage = {}

	with open(config.div_paths["sett"], "r") as sett_txt:
		settList = sett_txt.read().split("\n")
	for sett in settList:
		if sett == "!":
			break
		else:
			name, val = sett.split(":")
			if val[-2:] == "_b":
				val = bool(int(val[:-2]))
			elif val[-2:] == "_i":
				val = int(val[:-2])
			elif val[-2:] == "_f":
				val = float(val[:-2])
			elif val[-2:] == "_s":
				val = val[:-2]
			elif val[-2:] == "_x":
				val = int(val[:-2], 16)
			else:
				val = None
			settings[name] = val

	if not settings["DEVTOOLS"]:
		settings["CHEATS"] = 0
	with open(config.div_paths["lang"], "r") as txtLang:
		text = txtLang.read()
	langs = {}
	for lang in text.split("#"):
		words = lang.split("\n")
		words = [w for w in words if w != ""]
		lang = words[0]
		langs[lang] = {}
		words = words[1:]
		for word in words:
			name, value = word.split("~")
			langs[lang][name] = value
	language = langs[settings["LANGUAGE"]]

	try:
		with open(config.div_paths["stats"], "rb") as statsFile:
			stats = pickle.Unpickler(statsFile).load()
	except IOError:
		firstLaunch = True
		stats = config.stats_default

	if settings["FPS_ADAPTATION"] in ("30", "60"):
		FPS = int(settings["FPS_ADAPTATION"])

def saveStats():

	if settings["CHEATS"] == 0:
		with open(config.div_paths["stats"], "wb") as statsFile:
			pickle.Pickler(statsFile).dump(stats)
		print("[LOG] Sauvegarde des données effectuées avec succès.")
	else:
		print("[LOG] Interdiction de sauvegarder (cheats).")

def get_cheat(i):

	i = 7-i
	binStr = "{0:b}".format(settings["CHEATS"])
	if len(binStr) < 8:
		binStr = "0"*(8-len(binStr))+binStr
	return binStr[i] == "1"

# NO SCORE REDUCTION ; DESTROY EVERYTHING ; GHOST ; MULTIPLESHOOT ; CRAZYSHOOTER ; SPEEED ; GIGADMG ; GODMODE
#         8                    4              2           1       ;      8            4        2         1

class SoundMananger:

	def __init__(self):

		pygame.mixer.set_num_channels(16)
		self.medias = {}
		self.loops = {}
		self.random_musics = []
		self.music1 = None
		self.music2 = None
		self.musicTime = 0
		for name, sound in config.sounds_dict.items():
			media = pygame.mixer.Sound("audio/{}.wav".format(sound))
			self.medias[name] = media
		for area, music in config.musics.items():
			if area == "main_music":
				self.music1 = [pygame.mixer.Sound(music[0]), music[1]]
			elif area == "victory_music":
				self.music2 = [pygame.mixer.Sound(music[0]), music[1]]
			elif area == "game_musics":
				try:
					for name, sec in music:
						media = pygame.mixer.Sound(name)
						self.random_musics.append([media, sec])
				except:
					print("[ERREUR] Echec du chargement des musiques de jeu")
		self.activeMusic = None
		self.set_volume()

	def played(self, sound):

		return self.medias[sound].get_num_channels() > 0

	def update(self):

		if self.activeMusic is not None:
			if time()-self.musicTime >= self.activeMusic[0].get_length()-self.activeMusic[1]:
				self.musicTime = time()
				self.activeMusic[0].play()
		for loop in self.loops.values():
			loop.update()

	def playSound(self, sound):

		if self.played(sound):
			self.medias[sound].stop()
		self.medias[sound].play()

	def stopSound(self, sound):

		if sound in self.medias:
			self.medias[sound].stop()

	def playMusic(self, music=0):

		self.stopMusic()
		if music == 1:
			self.activeMusic = self.music1
			fade = 3000
		elif music == 2:
			self.activeMusic = self.music2
			fade = 0
		else:
			self.activeMusic = choice(self.random_musics)
			fade = 1500
		self.musicTime = time()
		self.activeMusic[0].play(fade_ms=fade)

	def stopMusic(self):

		if self.activeMusic is not None:
			self.activeMusic[0].fadeout(500)
			self.activeMusic = None
		self.musicTime = 0

	def stopAll(self):

		self.stopMusic()
		for loop in self.loops.values():
			loop.hold = 0

	def set_volume(self):

		for media in self.medias.values():
			media.set_volume(settings["FXVOL"]*settings["GLOBALVOL"])
		for music in self.random_musics:
			music[0].set_volume(settings["MUSICVOL"]*settings["GLOBALVOL"])
		self.music1[0].set_volume(settings["MUSICVOL"]*settings["GLOBALVOL"])
		self.music2[0].set_volume(settings["MUSICVOL"]*settings["GLOBALVOL"])

	def create_sound_loops(self):

		for name in self.medias:
			self.loops[name] = self.soundLoop(name)

	def hold_loop(self, sound, vol):

		if self.loops[sound].hold < 5:
			self.loops[sound].hold = 5
			if vol > 0:
				self.loops[sound].sound.set_volume(settings["FXVOL"]*settings["GLOBALVOL"]*vol)

	class soundLoop:

		def __init__(self, sound):

			self.sound = soundMananger.medias[sound]
			self.inter = self.sound.get_length()*0.75
			self.time = time()
			self.hold = 0
			self.activated = False

		def update(self):

			if self.hold == 0:
				if self.activated:
					self.sound.stop()
					self.activated = False
			else:
				self.hold -= 1
				if not self.activated:
					self.activated = True
					self.sound.play()
					self.time = time()
				if self.sound.get_num_channels() == 0:
					self.sound.play()
				if time()-self.time >= self.inter:
					self.sound.fadeout(int(self.inter*0.5*1000))
					self.time = time()
					self.sound.play(fade_ms=int(self.inter/2*1000))

def create_soundMananger():

	global soundMananger
	soundMananger = SoundMananger()
	soundMananger.create_sound_loops()

def save_settings():

	global FPS

	typeList = []
	with open(config.div_paths["sett"], "r") as settFile:
		for sett in settFile.read().split("\n"):
			if sett != "!":
				typeList.append(sett[-2:])
	text = ""
	i = 0
	for name, val in settings.items():
		if typeList[i] == "_b":
			val = int(val)
		elif typeList[i] == "_x":
			val = "{0:x}".format(val)
		text += "{}:{}{}\n".format(name, val, typeList[i])
		i += 1
	text += "!"
	with open(config.div_paths["sett"], "w") as settFile:
		settFile.write(text)

	if settings["FPS_ADAPTATION"] in ("30", "60"):
		FPS = int(settings["FPS_ADAPTATION"])

def display_win_update():

	if settings["WINSIZE"] == "AUTO":
		width = windll.user32.GetSystemMetrics(0)
		height = windll.user32.GetSystemMetrics(1)
	elif settings["WINSIZE"] == "DEFAULT":
		width, height = GAMEVALUES.defaultWinSize
	else:
		width, height = settings["WINSIZE"].split("x")
		width, height = int(width), int(height)

	if width > GAMEVALUES.defaultWinSize[0]:
		width = GAMEVALUES.defaultWinSize[0]
	elif width < GAMEVALUES.defaultWinSize[0]/4:
		width = GAMEVALUES.defaultWinSize[0]/4
	if height > GAMEVALUES.defaultWinSize[1]:
		height = GAMEVALUES.defaultWinSize[1]
	elif height < GAMEVALUES.defaultWinSize[1]/4:
		height = GAMEVALUES.defaultWinSize[1]/4

	pygame.display.set_mode((width, height))
	if settings["FULLSCREEN"]:
		try:
			pygame.display.set_mode((width, height), FULLSCREEN)
		except pygame.error:
			print("[ERREUR] ERREUR PLEIN ECRAN")

def get_diff(id):

	if id == 0:
		return "diff_challenge"
	elif id == 1:
		return "diff_hard"
	elif id == 2:
		return "diff_normal"
	elif id == 3:
		return "diff_easy"
	elif id == 4:
		return "diff_s-challenge"
	elif id == 5:
		return "diff_s-easy"

def openUrl(name):

	if settings["FULLSCREEN"]:
		settings["FULLSCREEN"] = False
		display_win_update()
		save_settings()
	webbrowser.open(config.urls[name])
