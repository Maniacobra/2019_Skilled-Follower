# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random
from copy import copy

import game_values as GAMEVALUES
from proj_models import projectile_models
from visuals import *
from fct import *
from projectile import *
import res
import specialObjects_1, \
specialObjects_2, \
specialObjects_3, \
specialObjects_4, \
specialObjects_5

specialDict = {
"shooting":specialObjects_1.shooting,
"duo_shooting":specialObjects_1.duo_shooting,
"multipleShooting":specialObjects_1.multipleShooting,
"randShoot":specialObjects_1.randShoot,
"seqShoot":specialObjects_1.seqShoot,
"anim":specialObjects_3.anim,
"randRot":specialObjects_3.randRot,
"megaShoot":specialObjects_2.megaShoot,
"rotate":specialObjects_3.rotate,
"colorShape":specialObjects_3.colorShape,
"lazer":specialObjects_2.lazer,
"destroySignal":specialObjects_4.destroySignal,
"hitSignal":specialObjects_4.hitSignal,
"zoneSignal":specialObjects_4.zoneSignal,
"clockSignal":specialObjects_4.clockSignal,
"signalCondition":specialObjects_4.signalCondition,
"delaySignal":specialObjects_4.delaySignal,
"contact_button":specialObjects_3.contact_button,
"door":specialObjects_3.door,
"tp":specialObjects_5.tp,
"moving":specialObjects_5.moving,
"follMove":specialObjects_5.followMove,
"orbit":specialObjects_5.orbit,
"forceField":specialObjects_5.forceField,
"point":specialObjects_5.point,
"tesla":specialObjects_2.tesla,
}

class map_object(pygame.sprite.Sprite):

	def __init__(self, id, name, rect, texture, angle, model, scoreMlt):

		pygame.sprite.Sprite.__init__(self)
		self.pGEs = []
		self.id = id
		self.name = name
		self.texture = texture
		self.solid = model["k"][0]
		self.hazard = model["k"][1]
		self.hardness = model["h"]
		if self.hardness > -1:
			self.hardness *= ((1+scoreMlt)/2)
		if self.hardness == -1 and res.get_cheat(6) and self.name != "exit":
			self.hardness = 200
		self.shape = model["sh"]
		self.imgName = model["name"]
		self.angle = angle
		self.ortho_angle = orth_angle(angle)
		if self.imgName is not None:
			self.image = pygame.transform.rotate(res.images[self.imgName][texture], self.ortho_angle)
		else:
			self.image = None
		self.hpb_ran_circle_angle = random.randrange(0, 360)
		self.rect = copy(rect)
		self.hitbox = self.rect.inflate(model["hb"], model["hb"])
		self.damage = 0
		self.hp_bar = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.fixedRect = self.rect
		self.kBEffectTime = 0
		self.hpb_alpha = 0
		self.delete = False
		self.specials = []
		self.trigger = False
		self.points = model["pts"]+3/35*self.hardness
		self.fromPlayer = False
		self.collided = False
		self.partialGrid = None
		self.magic = False
		for spe in model["spe"].items():
			if spe[0] == "focusable":
				self.trigger = True
			else:
				speClass = specialDict[spe[0]]
				if spe[0] == "destroySignal":
					self.trigger = True
				self.specials.append(speClass(self, spe[1], scoreMlt))
		self.targeted = False
		self.miniCount = 1

	def update(self, A_G_V):

		for spe in self.specials:
			spe.update(self, A_G_V)

		self.miniCount -= 1
		if self.miniCount == 0:
			self.miniCount = 60

		if self.delete:
			if self.fromPlayer:
				A_G_V.points(self.points)
			if self.name != "exit":
				res.soundMananger.playSound("blockDestruction")
			for spe in self.specials:
				spe.endAction(self, A_G_V)
			if self.shape == 0:
				A_G_V.gameSprites["visuals"].add(whiteSquare(self.rect))
			elif self.shape == 1:
				A_G_V.gameSprites["visuals"].add(whiteCircle(self.rect))
			self.kill()
			return

		if self.kBEffectTime > 0:
			if self.kBEffectTime == 4:
				for spe in self.specials:
					spe.hitAction(self, A_G_V)
				res.soundMananger.playSound("projectileHit")
			self.kBEffectTime -= 1
			if self.kBEffectTime == 0:
				self.rect = self.fixedRect

		if self.hpb_alpha > 0:
			self.hpb_alpha -= 10

		self.collided = False

	def draw(self, window):

		for spe in self.specials:
			spe.sdraw(window, self.fixedRect)
		if self.image is not None:
			window.blit(self.image, self.rect)
		for spe in self.specials:
			spe.draw(window, self.rect)
		if self.hpb_alpha > 0:
			blit_alpha(window, self.hp_bar, self.rect, self.hpb_alpha)

	def collide(self, rect):

		if self.shape == 0:
			return circleRect_collision(self.hitbox, rect.w/2, rect.center)
		elif self.shape == 1:
			return collideCircle(self.hitbox, rect)

	def hit(self, damages, knockbackEffect, fromPlayer=True):

		if self.hardness > 0:
			res.stats["totalDamages"] += damages
			self.damage += damages
			if self.shape == 0:
				self.hp_bar = draw_cornerBar(self.rect, self.hardness, self.damage)
			else:
				self.hp_bar = draw_circleBar(self.rect, self.hardness, self.damage, self.hpb_ran_circle_angle)
			self.hpb_alpha = 255
			if self.damage >= self.hardness:
				self.delete = True
				if fromPlayer:
					self.fromPlayer = True
					res.stats["blockDestroyed"] += 1
			else:
				self.rect = self.fixedRect.move(knockbackEffect[0]/3, knockbackEffect[1]/3)
				self.kBEffectTime = 4

	def set_pGE(self, partialGrid=None):

		self.pGEs = []
		if partialGrid is not None:
			self.partialGrid = partialGrid
		for rect in self.partialGrid[1].items():
			if pygame.Rect.colliderect(self.rect, rect[1]):
				self.pGEs.append(rect[0])

	def signal(self, signal):

		for spe in self.specials:
			spe.signal(signal, self)
		if signal == "destroy":
			self.delete = True

	def update_img(self, texture):

		self.texture = texture
		if self.texture < 0:
			self.texture = 0
		self.image = pygame.transform.rotate(res.images[self.imgName][texture], self.ortho_angle)

	def focused(self): self.targeted = True

	def unFocused(self): self.targeted = False
