# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import randint, shuffle
from time import time

import game_values as GAMEVALUES
from fct import *
from visuals import flash
import interface
import res

class MainMenu():

	def __init__(self, clock):

		self.redirect = None
		self.clock = clock

		self.gameLaunchArgs = GAMEVALUES.normal_mode
		self.diffNb = 2

		self.clickTxt = None
		if res.firstLaunch:
			self.clickTxt = res.fonts["simpleText"].render(res.language["rightClick"], 1, (255, 255, 255))
			self.diffNb = 3
			self.gameLaunchArgs = GAMEVALUES.easy_mode
			self.diffText = res.fonts["simpleText"].render(res.language["easy"], 1, (255, 255, 70))
		else:
			self.diffText = res.fonts["simpleText"].render(res.language["normal"], 1, (255, 255, 70))

		self.playButton = interface.button(res.language["play"], (683, 300))
		self.statsButton = interface.button(res.language["stats"], (683, 370))
		self.prefButton = interface.button(res.language["settings"], (683, 440))
		self.quitButton = interface.button(res.language["quit"], (683, 510))
		self.bgButton = interface.button(str(int(res.settings["MOVING_BG"])), (1336, 728))
		self.maniaButton = interface.button("maniacobra.com", (1235, 35), True)
		self.htpButton = interface.button(res.language["howToPlay"], (150, 728), True)
		self.allButtons = pygame.sprite.Group(self.playButton, self.prefButton, self.statsButton, self.quitButton, self.bgButton, self.maniaButton, self.htpButton)
		self.mailTxt = res.fonts["mainFont"].render("{} : {}".format(res.language["contact"], res.mail), 1, (255, 255, 255))

		self.titlePos = res.images["title"][0].get_rect(centerx=675, y=100)
		self.version = res.fonts["simpleText"].render(GAMEVALUES.version, 1, (200, 200, 200))
		self.copyright = res.fonts["simpleText"].render("© Maniacobra 2019", 1, (200, 200, 200))

		self.transition = pygame.sprite.GroupSingle(flash((0, 0, 0), 255, 30))

	def update(self, animBg):

		animBg.update()
		self.titlePos.centerx = 675
		self.titlePos.y = 100
		self.titlePos = self.titlePos.move(randint(0, 3)-1, randint(0, 3)-1)

		for event in pygame.event.get():
			if event.type == QUIT:
				self.redirect = "q"
			elif event.type == MOUSEMOTION:
				for butt in self.allButtons:
					butt.mousePos = scalePos(event.pos)
			elif event.type == KEYDOWN and event.key == K_RETURN and res.settings["DEVTOOLS"]:
				self.redirect = "launchTest"
			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				if (res.stats["diff_normal"][1] > 0 or res.stats["diff_hard"][1] > 0 or 0 < self.diffNb < 4) and self.playButton.click():
					self.redirect = "launchGame"
					if res.firstLaunch:
						self.redirect = "tuto_launch"
				elif self.statsButton.click():
					self.redirect = "stats"
				elif self.prefButton.click():
					self.redirect = "sett"
				elif self.quitButton.click():
					self.redirect = "q"
				elif self.htpButton.click():
					self.redirect = "tuto"
				elif self.bgButton.click():
					if res.settings["MOVING_BG"]:
						res.settings["MOVING_BG"] = False
					else:
						res.settings["MOVING_BG"] = True
					self.bgButton.changeText(str(int(res.settings["MOVING_BG"])))
					res.save_settings()
				elif self.maniaButton.click():
					res.openUrl("web")
			elif event.type == MOUSEBUTTONDOWN and event.button == 3 and self.playButton.mouseOn:
				self.clickTxt = None
				res.soundMananger.playSound("click")
				self.diffNb -= 1
				if self.diffNb < 0:
					self.diffNb = 4
				if self.diffNb == 0:
					self.gameLaunchArgs = GAMEVALUES.challenge_mode
					diffStr = "challenge"
					if res.stats["diff_normal"][1] == 0 and res.stats["diff_hard"][1] == 0:
						self.playButton.changeText(res.language["locked"], True)
				elif self.diffNb == 1:
					self.gameLaunchArgs = GAMEVALUES.hard_mode
					diffStr = "hard"
				elif self.diffNb == 2:
					self.gameLaunchArgs = GAMEVALUES.normal_mode
					diffStr = "normal"
				elif self.diffNb == 3:
					self.gameLaunchArgs = GAMEVALUES.easy_mode
					diffStr = "easy"
					self.playButton.changeText(res.language["play"], False)
				elif self.diffNb == 4:
					self.gameLaunchArgs = GAMEVALUES.s_challenge_mode
					diffStr = "s-challenge"
					if res.stats["diff_normal"][1] == 0 and res.stats["diff_hard"][1] == 0:
						self.playButton.changeText(res.language["locked"], True)
				elif self.diffNb == 5:
					self.gameLaunchArgs = GAMEVALUES.s_easy_mode
					diffStr = "s-easy"
					self.playButton.changeText(res.language["play"], False)
				self.diffText = res.fonts["simpleText"].render(res.language[diffStr], 1, (255, 255, 70))

		self.allButtons.update()
		self.transition.update()

	def show(self, window, animBg):

		animBg.draw(window)
		window.blit(self.version, (0, 0))
		window.blit(self.copyright, (0, 15))
		window.blit(res.images["title"][0], self.titlePos)
		self.allButtons.draw(window)
		if self.playButton.mouseOn:
			diffTextRect = self.diffText.get_rect(centery=self.playButton.rect.y-6)
			diffTextRect.centerx = self.playButton.rect.centerx+10
			dtc_border = diffTextRect.inflate(16, 10)
			window.fill((50, 50, 50), dtc_border)
			pygame.draw.rect(window, (200, 200, 200), dtc_border, 2)
			window.blit(self.diffText, diffTextRect)
			if self.clickTxt is not None:
				window.blit(self.clickTxt, (775, 290))

		self.transition.draw(window)

	def reinit(self):

		self.redirect = None
		for butt in self.allButtons:
			butt.reinit()

class TutoMenu():

	def __init__(self, lg=False):

		self.redirect = None
		self.slide = 0
		self.launchGame = lg
		self.dedis = None

	def update(self):

		for event in pygame.event.get():
			if event.type == QUIT:
				self.redirect = "q"
			elif event.type == MOUSEBUTTONDOWN and event.button in (1, 3):
				res.soundMananger.playSound("click")
				self.slide += 1
				if self.slide == 3:
					if self.launchGame:
						self.redirect = "launchGame"
						self.launchGame = False
					else:
						self.redirect = "main"
					self.slide = 2

	def show(self, window):

		if self.dedis is None:
			window.blit(res.images["tutorial"][self.slide], (0, 0))
		else:
			window.blit(self.dedis, (0, 0))
