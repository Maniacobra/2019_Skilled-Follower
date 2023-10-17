# -*- coding: utf-8 -*-

import math
import pygame
from pygame.locals import *
import os
import random
import sys
from time import time
from threading import Thread

import game_values as GAMEVALUES
from player import player
from map_object import map_object
from projectile import projectile
from visuals import *
from fct import *
import interface
import res

class ActiveGameValues():

	def __init__(self, gameSprites, score, scoreMultiplier, partialGrid, lifes):

		self.gameSprites = gameSprites
		self.partialGrid = partialGrid
		self.mousePos = scalePos(pygame.mouse.get_pos())
		self.unlock = False
		self.end = None
		self.score = score
		self.scoreMultiplier = scoreMultiplier
		self.exitClose = False
		self.lifes = lifes
		self.positivePoints = 0
		self.negativePoints = 0
		for obj in self.gameSprites["objects"]:
			if obj.name == "exit" and obj.hardness > 0:
				self.exitClose = True
				obj.imgName = "exit_close"
				obj.update_img(0)
				obj.signal("stopAnim")

	def loose(self):

		if not res.get_cheat(0) and self.unlock:
			hurtTest = self.gameSprites["player"].hurt()
			if hurtTest == 2:
				self.points(GAMEVALUES.shieldPts)
				if self.lifes > 1:
					self.lifes -= 1
			elif not hurtTest:
				self.gameSprites["player"].unFocus()
				self.end = "loose"
				res.stats["deaths"] += 1
				return True
			return False

	def win(self):

		if not self.exitClose:
			if self.scoreMultiplier < 1:
				self.score += GAMEVALUES.winPts
			else:
				self.score += GAMEVALUES.winPts*self.scoreMultiplier
			self.end = "next"
			res.stats["levelsCompleted"] += 1

	def addProj(self, proj, hazard=False):

		if len(self.gameSprites["projectiles"]) < 1000:
			proj.set(self.partialGrid, self.scoreMultiplier)
			self.gameSprites["projectiles"].add(proj)
			if hazard:
				self.gameSprites["hazardProjectiles"].add(proj)

	def addProj_args(self, *args):

		if len(self.gameSprites["projectiles"]) < 1000:
			proj = projectile(*args)
			proj.set(self.partialGrid, self.scoreMultiplier)
			self.gameSprites["projectiles"].add(proj)
			self.gameSprites["hazardProjectiles"].add(proj)

	def addLayerDeco(self, obj):

		if res.settings["COLOR_LAYERS"]:
			self.gameSprites["forefront_visuals"].add(obj)

	def points(self, points):

		points = points*self.scoreMultiplier
		self.score += points
		if points > 0:
			res.stats["totalScore"] += points
			self.positivePoints += points
		else:
			self.negativePoints -= points

	def sendSignal(self, targets, signals):

		if signals == "OPEN_EXIT" and self.exitClose:
			for obj in self.gameSprites["objects"]:
				if obj.name == "exit" and obj.hardness > 0:
					self.gameSprites["visuals"].add(growingCircle(obj.rect.move(5, 5).center, 175, 1))
					self.gameSprites["visuals"].add(whiteCircle(obj.rect))
					obj.imgName = "exit"
					obj.update_img(0)
					obj.signal("startAnim")
			res.soundMananger.playSound("exit_open")
			self.exitClose = False
		else:
			signals = signals.split("/")
			targets = targets.split("/")
			if len(signals) < len(targets):
				for i in range(len(targets)-len(signals)):
					signals.append(signals[0])
			i = 0
			for tar in targets:
				for obj in self.gameSprites["objects"]:
					if obj.id == tar:
						obj.signal(signals[i])
				i += 1

	def get_solids(self, mode=0):

		if mode == 1 and not self.gameSprites["player"].outStart:
			return [obj for obj in self.gameSprites["objects"] if obj.solid or obj.name == "start"]
		elif mode == 2:
			return [obj for obj in self.gameSprites["objects"] if obj.solid and not obj.hazard]
		return [obj for obj in self.gameSprites["objects"] if obj.solid]

	def get_hazards(self):

		return [obj for obj in self.gameSprites["objects"] if obj.hazard]

	def get_destroyable(self, hpMin=1, desSin=False):

		if desSin:
			return [obj for obj in self.get_solids() if obj.hardness >= hpMin or obj.trigger]
		return [obj for obj in self.get_solids() if obj.hardness >= hpMin]

class Game():

	def __init__(self, diff, Level, mapName, stage, clock, startFlash, shield, scoreMultiplier, lifes, score=None, chrono=0.0):

		self.fpsText = "FPS : --.--"
		self.fpsTextColor = (255, 255, 255)

		if score is None:
			score = GAMEVALUES.startPts
			if score < 130:
				score = 130

		chronoText = res.fonts["digital"].render(res.language["time"], 1, (250, 250, 250))
		scoreText = res.fonts["digital"].render(res.language["score"], 1, (250, 250, 250))
		lifesText = res.fonts["digital"].render(res.language["lifes"], 1, (250, 250, 250))
		self.sb_text = pygame.Surface(res.images["scorebar"][0].get_rect().size, pygame.SRCALPHA).convert_alpha()
		self.sb_text.blit(res.fonts["digital"].render("{} {}/{}".format(res.language["level"], stage, GAMEVALUES.level_nb), 1, (250, 250, 255)), (10, 4))
		self.sb_text.blit(chronoText, chronoText.get_rect(topright=(273, 4)))
		self.sb_text.blit(scoreText, scoreText.get_rect(topright=(498, 4)))
		self.sb_text.blit(lifesText, lifesText.get_rect(topright=(688, 4)))

		self.mapName = mapName
		self.stage = stage
		self.clock = clock
		self.chrono = chrono
		self.pauseMenu = None

		partialGrid = create_partial_grid((1366, 768), 8, 5)
		self.exitPos = Level["pos"][1]
		self.objects = Level["obj"].copy()
		for obj in self.objects:
			obj.set_pGE(partialGrid)
			if obj.name == "start":
				obj.focused()
		self.projectiles = pygame.sprite.Group()
		self.hazardProjectiles = pygame.sprite.Group()
		self.particles = particleLayer(res.settings["MAX_PARTICLES"], res.settings["PARTICLES_FRAMES_UPDATE"])
		self.visuals = pygame.sprite.Group()
		self.forefront_visuals = pygame.sprite.Group()
		player_pGE = []
		for rect in partialGrid[1].items():
			if rect[1].collidepoint(Level["pos"][0]):
				player_pGE.append(rect[0])
		self.player = player(Level["pos"][0], self.exitPos, shield, player_pGE)
		if lifes < 2:
			self.player.shield = False

		gameSprites = {
		"exitPos":self.exitPos, \
		"player":self.player, \
		"objects":self.objects, \
		"projectiles":self.projectiles, \
		"hazardProjectiles":self.hazardProjectiles, \
		"visuals":self.visuals, \
		"forefront_visuals":self.forefront_visuals, \
		"particles":self.particles}
		self.A_G_V = ActiveGameValues(gameSprites, score, scoreMultiplier, partialGrid, lifes)

		self.endMessage = res.fonts["buttons"].render(res.language["end{}".format(random.randint(1, 16))], 1, (255, 255, 255))
		self.endTxt = res.fonts["mainFont"].render("{} : {} {}".format(res.language[res.get_diff(diff)[5:]], res.language["level"], self.stage), 1, (255, 255, 255))
		self.showEnd = False
		self.particleCount = 40

		if startFlash == 0:
			self.A_G_V.addLayerDeco(flash())
		else:
			self.A_G_V.addLayerDeco(flash((0, 0, 0)))

		self.endWait = 301
		self.redirect = None

		self.startCd = 150

		self.profile = False
		self.devMode = False
		self.freezeDeath = pygame.Surface((1366, 768))
		self.fpsUpdate = time()

	def update(self):

		timeTest = time()

		if self.startCd > 0:
			self.startCd -= 1

		for event in pygame.event.get():

			if event.type == QUIT:
				self.redirect = "quit"

			elif event.type == KEYDOWN:
				print(event.key)
				if event.key == K_ESCAPE:
					self.pauseMenu = Pause(self.chrono)
					self.redirect = "pause"
				elif event.key == K_q:
					self.player.rotate(1)
				elif event.key == K_s:
					self.player.rotate(2)
				elif event.key == K_SPACE:
					self.player.focusBlock(self.A_G_V.get_destroyable(125, True))
				elif event.key == K_F11 and res.settings["DEVTOOLS"]:
					if self.devMode:
						self.devMode = False
					else:
						self.devMode = True
				elif event.key == K_F3 and res.settings["DEVTOOLS"]:
					self.profile = True
				elif event.key == K_LSHIFT:
					self.player.focusBlockDes()

			elif event.type == KEYUP:

				if event.key == K_q:
					self.player.unRotate(1)
				elif event.key == K_s:
					self.player.unRotate(2)
				elif event.key == K_SPACE:
					self.player.unRotate(3)

			elif event.type == MOUSEMOTION:

				self.A_G_V.mousePos = list(scalePos(event.pos))

			elif event.type == MOUSEBUTTONDOWN:
				if self.A_G_V.unlock == False and event.button in (1, 3):
					self.A_G_V.mousePos = list(scalePos(event.pos))
					self.A_G_V.unlock = True
					self.player.showCursor = True
				elif event.button == 1:
					self.player.shoot(1)
				elif event.button == 2:
					self.player.focusBlockDes()
				elif event.button == 3:
					self.player.shoot(2)
				elif event.button == 4:
					self.player.sDAngle = limitangle(self.player.sDAngle+15)
					self.player.unFocus()
				elif event.button == 5:
					self.player.sDAngle = limitangle(self.player.sDAngle-15)
					self.player.unFocus()

			elif event.type == MOUSEBUTTONUP:

				if event.button == 1:
					self.player.unShoot(1)
				elif event.button == 3:
					self.player.unShoot(2)

			elif event.type == ACTIVEEVENT and event.state == 1 and event.gain == 1:
				self.player.freeze = False

		if pygame.mouse.get_focused() == 0 and self.player.skin == 0:
			self.player.freeze = True

		if self.A_G_V.score <= 0 and self.stage > 0 and self.A_G_V.scoreMultiplier > 0.8:
			self.A_G_V.end = "t-loose"

		if self.A_G_V.end is None and self.A_G_V.unlock:
			self.chrono += 1/60
			res.stats["totalTime"] += 1/60
			passScore = int(self.A_G_V.score)
			if not res.get_cheat(7):
				self.A_G_V.points(-0.05)
			self.player.update(self.A_G_V)
			if int(self.A_G_V.score) < passScore:
				if self.A_G_V.score < 31*self.A_G_V.scoreMultiplier and int(self.A_G_V.score)%6 == 0:
					res.soundMananger.playSound("time")
				elif self.A_G_V.score < 16*self.A_G_V.scoreMultiplier and int(self.A_G_V.score)%3 == 0:
					res.soundMananger.playSound("time")
				elif self.A_G_V.score < 4*self.A_G_V.scoreMultiplier:
					res.soundMananger.playSound("time")
		self.objects.update(self.A_G_V)
		self.projectiles.update(self.A_G_V)
		self.particles.update()
		self.visuals.update()
		self.forefront_visuals.update()
		if self.A_G_V.end is not None:
			if self.endWait == 301:
				self.endWait = 100
				if self.A_G_V.end == "loose":
					self.A_G_V.lifes -= 1
					if self.A_G_V.lifes < 0:
						res.stats["gamesFailed"] += 1
						res.soundMananger.stopMusic()
						if self.stage > 1:
							self.endWait = 200
							self.showEnd = True
					res.soundMananger.stopSound("shieldLoss")
					res.soundMananger.playSound("playerDeath")
					self.forefront_visuals.add(tempEffect("a-playerDeath", 45, self.player.rect.center))
				elif self.A_G_V.end == "t-loose":
					self.A_G_V.lifes -= 1
					if self.A_G_V.lifes < 0:
						res.stats["gamesFailed"] += 1
						res.soundMananger.stopMusic()
					res.soundMananger.stopSound("shieldLoss")
					res.soundMananger.playSound("playerDeath")
					self.forefront_visuals.add(tempEffect("a-playerDeath", 60, self.player.rect.center))
				else:
					res.soundMananger.playSound("win")
					print("[INFO] Score du niveau {} : {}".format(self.stage, int(self.A_G_V.positivePoints-self.A_G_V.negativePoints)))
					self.player.unFocus()
					self.A_G_V.addLayerDeco(flash((255, 255, 255), 75, 30))
					for obj in self.objects:
						if obj.name == "exit":
							obj.delete = True
							break
			else:
				if self.A_G_V.end in ("loose", "t-loose"):
					if self.particleCount > 0:
						self.particleCount -= 1
						self.particles.add(self.endWait/10, self.endWait/2, self.player.rect.center, (150, 200, 255), 100, 30, 3)
					elif self.endWait == 15:
						self.A_G_V.addLayerDeco(fade((0, 0, 0)))
				else:
					if self.endWait == 15:
						self.A_G_V.addLayerDeco(fade())
				self.endWait -= 1
				if self.endWait == 0:
					if self.A_G_V.end == "t-loose":
						self.A_G_V.end = "loose"
					self.redirect = self.A_G_V.end

		actual_fps = self.clock.get_fps()
		tottMs = self.clock.get_rawtime()
		calcMs = str(tottMs)

		if time()-self.fpsUpdate >= 0.2:
			self.fpsUpdate = time()
			self.fpsTextColor = (120, 255, 120)
			if actual_fps < 60:
				self.fpsTextColor = (255, actual_fps/60*255, actual_fps/60*255)
			self.fpsText = "Gameplay FPS : {}".format(actual_fps.__round__(2))
			if len(calcMs) < 2:
				calcMs = "0" + calcMs
			self.fpsText += "!Display FPS : {}!Update : {}ms".format((actual_fps/(60/res.FPS)).__round__(2), calcMs)
			if res.FPS == 30:
				self.fpsText += "![ 50% UPDATE ]"

	def show(self, window):

		timeTest = time()

		window.blit(res.images["bg"][1], (0, 0))
		for obj in self.objects:
			obj.draw(window)
		for obj in self.objects:
			for spe in obj.specials:
				spe.fdraw(window, obj.fixedRect)
			if obj.targeted:
				if obj.name == "start":
					draw_select_area(window, obj.rect, obj.miniCount, 1, (255-obj.miniCount*3.5, 255-obj.miniCount*3, 255), 3)
				else:
					draw_select_area(window, obj.rect, obj.miniCount, obj.shape)
			elif obj.hardness > 135 and self.startCd > 0:
				draw_select_area(window, obj.rect, obj.miniCount, obj.shape, (255, 0, 0), 2)
		self.particles.draw(window)
		self.visuals.draw(window)
		self.projectiles.draw(window)
		if self.A_G_V.end is None:
			self.player.draw(window)

		scorebar = pygame.Surface(res.images["scorebar"][0].get_rect().size, pygame.SRCALPHA).convert_alpha()
		scorebar.blit(res.images["scorebar"][0], (0, 0))
		chrono_txt = res.fonts["digital"].render(espace1(convertTime2(self.chrono)), 1, (120, random.randint(120, 255), 120))
		randCol = randint(120,255)
		if self.A_G_V.score <= 0:
			score_txt = res.fonts["digital"].render("0.0", 1, (200, 100, 100))
		else:
			score_txt = res.fonts["digital"].render(espace1(self.A_G_V.score.__round__(1)), 1, (randCol, randCol, randCol))
		if self.A_G_V.lifes < 10:
			lifes_txt = res.fonts["digital"].render(str(self.A_G_V.lifes), 1, (120, 120, random.randint(120, 255)))
		else:
			lifes_txt = res.fonts["digital"].render("+", 1, (120, 120, random.randint(120, 255)))
		scorebar.blit(self.sb_text, (0, 0))
		scorebar.blit(chrono_txt, (280, 3))
		scorebar.blit(score_txt, score_txt.get_rect(topright=(598, 3)))
		if self.A_G_V.lifes >= 0:
			scorebar.blit(lifes_txt, lifes_txt.get_rect(topright=(719, 4)))

		if self.A_G_V.unlock and self.A_G_V.end is None:
			pygame.draw.circle(scorebar, (200, 200, 200), (388, 16), 5)
		if self.player.rect.colliderect(scorebar.get_rect()):
			opacity = 75
		else:
			opacity = 180
		blit_alpha(window, scorebar, (0, 0), opacity)

		if self.player.focusObj is not None and self.player.focusObj.damage < self.player.focusObj.hardness:
			hpText = res.fonts["digital"].render("HP : {}/{}".format(int(self.player.focusObj.hardness-self.player.focusObj.damage), int(self.player.focusObj.hardness)), 1, (255, 255, 255))
			hpRect = hpText.get_rect(topright=(1352, 11))
			opacRect = pygame.Surface((hpRect.width+20, 40))
			opacRect.set_alpha(125)
			window.blit(opacRect, (1346-hpRect.width, 0))
			window.blit(hpText, hpRect)

		if self.showEnd:
			blackBar = pygame.Surface((1366, 86))
			blackBar.set_alpha(170)
			window.blit(blackBar, (0, 336))
			window.blit(self.endMessage, self.endMessage.get_rect(center=(683, 364)))
			window.blit(self.endTxt, self.endTxt.get_rect(center=(683, 404)))

		self.forefront_visuals.draw(window)

		if self.devMode:
			window.fill((0, 0, 0))
			for rect in self.A_G_V.partialGrid[1].values():
				pygame.draw.line(window, (50, 50, 50), (rect.x-30, rect.y), (rect.x+30, rect.y))
				pygame.draw.line(window, (50, 50, 50), (rect.x, rect.y-30), (rect.x, rect.y+30))
			for obj in self.objects:
				if obj.solid and not obj.hazard:
					color = (255, 255, 255)
				elif obj.solid and obj.hazard:
					color = (200, 200, 100)
				elif not obj.solid and obj.hazard:
					color = (200, 150, 255)
				else:
					color = (50, 100, 50)
				if obj.shape == 1:
					pygame.draw.circle(window, color, obj.rect.center, int(obj.hitbox.w/2))
				else:
					pygame.draw.rect(window, color, obj.hitbox)
			pygame.draw.circle(window, (0, 255, 0), (self.exitPos), 20)
			for proj in self.projectiles:
				pygame.draw.circle(window, (255, 100, 0), proj.hitbox.center, int(proj.hitbox.w/2))
				pygame.draw.line(window, (255, 255, 255), proj.pos, (proj.pos[0]+proj.motion[0], proj.pos[1]+proj.motion[1]))
			pygame.draw.circle(window, (0, 0, 255), self.player.rect.center, 11)

		if pygame.key.get_pressed()[K_F1]:
			for text, rect in lineTexts(self.fpsText, 1, "simpleText", [1366, 0], 12, self.fpsTextColor):
				window.blit(text, rect)

		if pygame.key.get_pressed()[K_F2]:
			spritesNb = (len(self.objects), len(self.projectiles), len(self.visuals), len(self.particles.particles), len(self.forefront_visuals))
			infos = "Total sprites : {}!Map objects : {}!Projectiles : {}!Visuels B : {} ({} particles)!Visuels A : {}!Player Pos (partial grid) : {}"\
			.format(spritesNb[0]+spritesNb[1]+spritesNb[2]+spritesNb[3]+spritesNb[4]+1, spritesNb[0], spritesNb[1], spritesNb[2], spritesNb[3], spritesNb[4], self.player.pGEs)
			for text, rect in lineTexts(infos, 0, "impact", [0, 740], -20):
				pygame.draw.rect(window, (50, 50, 50), rect)
				window.blit(text, rect)

	def eventUpdate(self):

		self.A_G_V.mousePos = scalePos(pygame.mouse.get_pos())
		cl = pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_q]
		cr = pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_s]
		if not (cl and cr):
			self.player.unRotate()
			if cl:
				self.player.rotate(1)
			elif cr:
				self.player.rotate(2)
		if not (pygame.mouse.get_pressed()[0] and pygame.mouse.get_pressed()[2]):
			self.player.unShoot()
			if pygame.mouse.get_pressed()[0]:
				self.player.shoot(1)
			elif pygame.mouse.get_pressed()[2]:
				self.player.shoot(2)

class Pause:

	def __init__(self, chrono):

		self.redirect = None

		self.fadeEffect = pygame.sprite.GroupSingle()
		self.leaveCD = 31
		self.opacLayer = pygame.Surface((1366, 768))
		self.opacLayer.fill((0, 0, 0))
		self.opacLayer.set_alpha(180)
		self.pauseTitle = res.fonts["title"].render("Pause", 1, (255, 255, 255))
		self.time = res.fonts["mainFont"].render(convertTime2(chrono), 1, (255, 255, 255))
		self.restartButton = interface.button(res.language["restart"], (683, 430))
		self.leaveButton = interface.button(res.language["mainmenu"], (683, 570))
		self.continueButton = interface.button(res.language["continue"], (683, 360))
		self.settButton = interface.button(res.language["settings"], (683, 500))
		self.allButtons = pygame.sprite.Group(self.leaveButton, self.continueButton, self.restartButton, self.settButton)

	def update(self):

		active = self.leaveCD == 31
		for event in pygame.event.get():
			if event.type == QUIT:
				self.redirect = "quit"
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE and active:
					self.redirect = "continue"
				elif event.key == K_RETURN:
					self.redirect = "leave"
				elif event.key == K_TAB and active:
					self.redirect = "restart"
			elif event.type == MOUSEMOTION:
				for butt in self.allButtons:
					butt.mousePos = scalePos(event.pos)
			elif event.type == MOUSEBUTTONDOWN and event.button == 1 and active:
				if self.leaveButton.click():
					if res.settings["COLOR_LAYERS"]:
						self.fadeEffect.add(fade((0, 0, 0), 255, 30))
					self.leaveCD = 30
				elif self.continueButton.click():
					self.redirect = "continue"
				elif self.restartButton.click():
					self.redirect = "restart"
				elif self.settButton.click():
					self.redirect = "pauseSett"
		if active:
			self.allButtons.update()
		else:
			if self.leaveCD > 0:
				self.fadeEffect.update()
				self.leaveCD -= 1
			else:
				self.redirect = "leave"

	def show(self, window):

		window.blit(self.opacLayer, (0, 0))
		window.blit(self.pauseTitle, self.pauseTitle.get_rect(centerx=683, y=100))
		window.blit(self.time, self.time.get_rect(centerx=683, y=200))
		self.allButtons.draw(window)
		self.fadeEffect.draw(window)

	def reinit(self):

		self.redirect = None
		for butt in self.allButtons:
			butt.reinit()
