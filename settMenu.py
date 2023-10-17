# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import choice

import game_values as GAMEVALUES
from fct import *
import interface
import res

class SettingsMenu:

	def __init__(self):

		self.redirect = None

		fs = "off"
		if res.settings["FULLSCREEN"]:
			fs = "on"
		wb_txt = res.language["auto"]
		if res.settings["WINSIZE"] == "DEFAULT":
			wb_txt = "{} {}".format(res.language["default"], GAMEVALUES.defaultWinSize)
		elif res.settings["WINSIZE"] == "1024x576":
			wb_txt = "1024x576"
		elif res.settings["WINSIZE"] == "AUTO":
			wb_txt = res.language["auto"]
		self.leaveButton = interface.button(res.language["ok"], (683, 720))
		self.fsButton = interface.button("{} : {}".format(res.language["fullscreen"], res.language[fs]), (683, 100), True)
		self.winButton = interface.button("{} : {}".format(res.language["winSize"], wb_txt), (683, 150), True)
		self.soundSlider = interface.slider(270, res.settings["FXVOL"])
		self.volSlider = interface.slider(350, res.settings["GLOBALVOL"])
		self.langButton = interface.button("{} : {}".format(res.language["language"], res.settings["LANGUAGE"]), (683, 430), True)
		self.graphButton = interface.button("{} : {}".format(res.language["part_lvl"], res.settings["GRAPHS"]), (683, 515), True)
		if res.settings["FPS_ADAPTATION"] == "AUTO":
			self.fpsButton = interface.button("{} : {}".format(res.language["fps_adapt"], res.settings["FPS_ADAPTATION"]), (683, 570), True)
		else:
			self.fpsButton = interface.button("{} : {} FPS {}".format(res.language["fps_adapt"], res.settings["FPS_ADAPTATION"], res.language["only"]), (683, 570), True)

		self.allButtons = pygame.sprite.Group(self.leaveButton, self.fsButton, self.winButton, self.langButton, self.graphButton, self.fpsButton)

		self.soundSliderTxt = res.fonts["smallButtons"].render(res.language["soundvol"], 1, (255, 255, 255))
		self.volSliderTxt = res.fonts["smallButtons"].render(res.language["globalvol"], 1, (255, 255, 255))
		self.languageInfoTxt = res.fonts["simpleText"].render(res.language["languageInfo"], 1, (255, 255, 255))
		self.graphInfoTxt = res.fonts["simpleText"].render(res.language["graphInfo"], 1, (255, 255, 255))
		self.graphInfoTxt2 = res.fonts["simpleText"].render(res.language["recommended"], 1, (255, 255, 255))
		self.lang_changed = False

		self.opacLayer = pygame.Surface((1366, 768))
		self.opacLayer.fill((0, 0, 0))
		self.opacLayer.set_alpha(180)

	def update(self, animBg=None):

		if animBg is not None:
			animBg.update()
		for event in pygame.event.get():

			if event.type == QUIT:
				self.redirect = "q"

			elif event.type == MOUSEMOTION:
				for butt in self.allButtons:
					butt.mousePos = scalePos(event.pos)
				if self.soundSlider.catched and res.settings["GLOBALVOL"] > 0:
					ratio = self.soundSlider.slide(scalePos(event.pos)[0])
					res.settings["FXVOL"] = ratio
					res.settings["MUSICVOL"] = 1-ratio
					res.soundMananger.set_volume()
				elif self.volSlider.catched:
					res.settings["GLOBALVOL"] = self.volSlider.slide(scalePos(event.pos)[0])
					res.soundMananger.set_volume()

			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				if animBg is None:
					self.redirect = "pause"
				else:
					self.redirect = "main"

			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				if res.settings["GLOBALVOL"] > 0:
					self.soundSlider.catch(event.pos)
				self.volSlider.catch(event.pos)
				if self.fsButton.click():
					if not res.settings["FULLSCREEN"]:
						res.settings["FULLSCREEN"] = True
						self.fs = "on"
					else:
						res.settings["FULLSCREEN"] = False
						self.fs = "off"
					self.fsButton.changeText("{} : {}".format(res.language["fullscreen"], res.language[self.fs]))
					self.fsButton.mousePos = scalePos(pygame.mouse.get_pos())
					res.display_win_update()
					res.save_settings()
				elif self.leaveButton.click():
					self.redirect = "main"
				elif self.winButton.click():
					wb_txt = res.language["auto"]
					if res.settings["WINSIZE"] == "AUTO":
						res.settings["WINSIZE"] = "DEFAULT"
						wb_txt = "{} {}".format(res.language["default"], GAMEVALUES.defaultWinSize)
					elif res.settings["WINSIZE"] == "DEFAULT":
						res.settings["WINSIZE"] = "1024x576"
						wb_txt = "1024x576"
					elif res.settings["WINSIZE"] == "1024x576":
						res.settings["WINSIZE"] = "AUTO"
						wb_txt = res.language["auto"]
					else:
						res.settings["WINSIZE"] = "AUTO"
					self.winButton.changeText("{} : {}".format(res.language["winSize"], wb_txt))
					res.display_win_update()
					res.save_settings()
				elif self.langButton.click():
					if res.settings["LANGUAGE"] == "FR":
						res.settings["LANGUAGE"] = "EN"
					else:
						res.settings["LANGUAGE"] = "FR"
					self.langButton.changeText("{} : {}".format(res.language["language"], res.settings["LANGUAGE"]))
					res.save_settings()
					self.lang_changed = True
				elif self.graphButton.click():
					if int(res.settings["GRAPHS"]) == 0:
						res.settings["GRAPHS"] = 1
						res.settings["MAX_PARTICLES"] = 2000
						res.settings["PARTICLES_FRAMES_UPDATE"] = 3
						res.settings["PART_SIZE"] = 4
						res.settings["PART_NB_MULT"] = 0.75
						res.settings["COLOR_LAYERS"] = True
					elif int(res.settings["GRAPHS"]) == 1:
						res.settings["GRAPHS"] = 2
						res.settings["MAX_PARTICLES"] = 5000
						res.settings["PARTICLES_FRAMES_UPDATE"] = 2
						res.settings["PART_SIZE"] = 4
						res.settings["PART_NB_MULT"] = 1
					elif int(res.settings["GRAPHS"]) == 2:
						res.settings["GRAPHS"] = 3
						res.settings["MAX_PARTICLES"] = 10000
						res.settings["PARTICLES_FRAMES_UPDATE"] = 1
						res.settings["PART_SIZE"] = 4
						res.settings["PART_NB_MULT"] = 1
					elif False:
						res.settings["GRAPHS"] = 4
						res.settings["MAX_PARTICLES"] = 20000
						res.settings["PARTICLES_FRAMES_UPDATE"] = 1
						res.settings["PART_SIZE"] = 2
						res.settings["PART_NB_MULT"] = 3
					else:
						res.settings["GRAPHS"] = 0
						res.settings["MAX_PARTICLES"] = 0
						res.settings["PARTICLES_FRAMES_UPDATE"] = 2
						res.settings["PART_SIZE"] = 4
						res.settings["PART_NB_MULT"] = 1
						res.settings["COLOR_LAYERS"] = False
					self.graphButton.changeText("{} : {}".format(res.language["part_lvl"], res.settings["GRAPHS"]))
					res.save_settings()
					if animBg is None:
						self.redirect = "changeGraph"
				elif self.fpsButton.click():
					if res.settings["FPS_ADAPTATION"] == "AUTO":
						res.settings["FPS_ADAPTATION"] = "60"
						self.fpsButton.changeText("{} : {} FPS {}".format(res.language["fps_adapt"], 60, res.language["only"]))
					elif res.settings["FPS_ADAPTATION"] == "60":
						res.settings["FPS_ADAPTATION"] = "30"
						self.fpsButton.changeText("{} : {} FPS {}".format(res.language["fps_adapt"], 30, res.language["only"]))
					else:
						res.settings["FPS_ADAPTATION"] = "AUTO"
						self.fpsButton.changeText("{} : AUTO".format(res.language["fps_adapt"]))
					res.save_settings()

			elif event.type == MOUSEBUTTONUP:
				if self.soundSlider.uncatch() or self.volSlider.uncatch():
					res.soundMananger.playSound(choice(list(res.soundMananger.medias.keys())))
					res.save_settings()

		self.allButtons.update()

	def show(self, window, animBg=None):

		if animBg is not None:
			animBg.draw(window)
		else:
			window.blit(self.opacLayer, (0, 0))
		self.allButtons.draw(window)
		self.soundSlider.draw(window)
		self.volSlider.draw(window)
		window.blit(res.images["symbols"][1], (462, 256))
		window.blit(res.images["symbols"][0], (873, 254))
		if res.settings["MUSICVOL"] == 0 or res.settings["GLOBALVOL"] == 0:
			pygame.draw.line(window, (255, 100, 100), (460, 285), (493, 254), 4)
		if res.settings["FXVOL"] == 0 or res.settings["GLOBALVOL"] == 0:
			pygame.draw.line(window, (255, 100, 100), (871, 285), (904, 254), 4)
		window.blit(self.soundSliderTxt, self.soundSliderTxt.get_rect(center=(683, 240)))
		window.blit(self.volSliderTxt, self.volSliderTxt.get_rect(center=(683, 320)))
		if self.lang_changed:
			window.blit(self.languageInfoTxt, self.languageInfoTxt.get_rect(center=(683, 395)))
		if res.settings["GRAPHS"] == 4:
			window.blit(self.graphInfoTxt, self.graphInfoTxt.get_rect(center=(683, 480)))
		elif res.settings["GRAPHS"] == 2:
			window.blit(self.graphInfoTxt2, self.graphInfoTxt2.get_rect(center=(683, 480)))

	def reinit(self):

		self.redirect = None
		for butt in self.allButtons:
			butt.reinit()
