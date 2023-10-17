# -*- coding: utf-8 -*-

import pygame
import math

import game_values as GAMEVALUES
from fct import *
from visuals import *
import res
import specialProjs

proj_specialDict = {
"unstable":specialProjs.electron,
"follow":specialProjs.follow,
"doubleVerif":specialProjs.doubleVerif,
"gravity":specialProjs.gravity,
"ghost":specialProjs.ghost,
"explode":specialProjs.explode,
"disappear":specialProjs.disappear,
"bounce":specialProjs.bounce,
"shooting":specialProjs.shooting,
}

class projectile(pygame.sprite.Sprite):

	def __init__(self, pos, angle, model):

		pygame.sprite.Sprite.__init__(self)
		self.id = model["n"]
		self.pGEs = []
		self.pGE = None
		self.speed = model["s"]
		self.motion = get_vect(angle, self.speed)
		self.image = pygame.transform.rotate(res.images["projectiles"][self.id], angle)
		self.rect = self.image.get_rect(center=pos)
		self.hitbox = pygame.Rect(0, 0, model["r"], model["r"])
		self.hitbox.center = pos
		self.damages = model["dmg"]
		if res.get_cheat(1) and self.damages > 0:
			self.damages *= 10
		self.delete = False
		self.magic = False
		self.desEffect = model["des"]
		self.desTime = model["dest"]
		self.trail = model["tr"]
		self.pos = list(pos)
		self.specials = []
		for spe in model["spe"].items():
			self.specials.append(proj_specialDict[spe[0]](self, spe[1]))

	def update(self, A_G_V):

		if self.pGE is None:
			self.kill()
			return
		if self.delete:
			for spe in self.specials:
				spe.endAction(self, A_G_V)
			if self.delete:
				if self.desEffect is not None:
					A_G_V.gameSprites["visuals"].add(tempEffect(self.desEffect, self.desTime, self.rect.center))
				self.kill()
		else:
			for spe in self.specials:
				spe.update(self, A_G_V)
			self.pos[0] += self.motion[0]
			self.pos[1] += self.motion[1]
			self.rect.center = self.pos
			self.hitbox.center = self.pos

			if self.trail is not None:
				A_G_V.gameSprites["particles"].add(self.trail["n"], self.trail["f"], self.rect.center, self.trail["c"], self.trail["o"], self.trail["z"], self.trail["d"])

			if not 5<self.pos[0]<1361 or not 5<self.pos[1]<763:
				self.kill()

			self.pGE, self.pGEs = pG_rectLeaving(self.rect, A_G_V.partialGrid[1][self.pGE], self.pGE)

			if not self.magic:
				testSprites = comparePGE(self.pGEs, A_G_V.get_solids(1))
				inflated = self.hitbox.inflate(5, 5)
				inflated.center = self.pos
				for obstacle in testSprites:
					if obstacle.collide(inflated):
						if self.damages > 0:
							A_G_V.gameSprites["player"].blockHit(obstacle)
							obstacle.hit(self.damages, self.motion)
						self.delete = True
						break

	def set(self, partialGrid, scoreMlt):

		for rect in partialGrid[1].items():
			if pygame.Rect.colliderect(self.rect, rect[1]):
				self.pGEs.append(rect[0])
		if len(self.pGEs) == 0:
			self.kill()
		else:
			self.pGE = self.pGEs[0]
		speedMult = (1+scoreMlt)/2
		if self.damages < 0 and self.speed*speedMult <= 30:
			self.motion[0] *= speedMult
			self.motion[1] *= speedMult
