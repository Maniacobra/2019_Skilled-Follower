#-*-coding:utf-8-*

import pygame
from pygame.locals import *
import math

import game_values as GAMEVALUES
from proj_models import projectile_models
from fct import *
from projectile import projectile
from visuals import *
import res

class player(pygame.sprite.Sprite):

	def __init__(self, pos, exitPos, shield, pGE):

		pygame.sprite.Sprite.__init__(self)

		self.cursorCircle = res.images["playerAttributes"][0]
		self.shootDirection = res.images["playerAttributes"][1]
		self.skins = res.images["player"]

		self.rect = self.skins[0].get_rect(center=(pos[0], pos[1]))
		self.rect = self.rect.inflate(-1, -1)
		self.pGE = pGE[0]
		self.pGEs = pGE
		self.skin = 6
		self.cCAngle = 0
		self.sDAngle = get_angle(self.rect.center, (683, 384))
		self.mouseDistance = 0
		self.shootCoolDown = 0
		self.shooting = 0
		self.speed = 1
		self.sDRotate = 0
		self.focusObj = None
		self.lastHit = None
		self.showCursor = False
		self.miniCount = 0
		self.pulse = 0, 0
		self.freeze = False
		self.noColl = False
		self.shield = False
		self.shieldTime = 0
		self.outStart = False
		self.shield = shield
		self.imgShield = rotativeDeco(res.images["playerAttributes"][2])

	def update(self, A_G_V):

		if not self.outStart:
			for obj in A_G_V.gameSprites["objects"]:
				if obj.name == "start" and not obj.collide(self.rect) or self.shooting != 0:
					self.outStart = True
					obj.unFocused()
		self.miniCount += 2
		if self.miniCount == 20:
			self.miniCount = 0
		deplaced = 0
		self.mouseDistance = int(distancePoint(self.rect.center, A_G_V.mousePos))
		maxSpeed = 9*self.speed
		if res.get_cheat(2):
			maxSpeed = 999
		move_vector = (A_G_V.mousePos[0]-(self.rect.centerx))*0.075, (A_G_V.mousePos[1]-(self.rect.centery))*0.075
		if math.fabs(move_vector[0]) > maxSpeed:
			move_vector = move_vector[0]*(maxSpeed/math.fabs(move_vector[0])), move_vector[1]*(maxSpeed/math.fabs(move_vector[0]))
		if math.fabs(move_vector[1]) > maxSpeed:
			move_vector = move_vector[0]*(maxSpeed/math.fabs(move_vector[1])), move_vector[1]*(maxSpeed/math.fabs(move_vector[1]))

		if self.freeze or distancePoint(self.rect.center, A_G_V.mousePos) < 40:
			move_vector = 0, 0

		movedPlayer = self.rect.move(move_vector)
		self.pGE, self.pGEs = pG_rectLeaving(movedPlayer.inflate(5, 5), A_G_V.partialGrid[1][self.pGE], self.pGE)

		if not self.noColl:
			hazards = comparePGE(self.pGEs, A_G_V.get_hazards())
			if self.shieldTime > 0:
				solids = comparePGE(self.pGEs, A_G_V.get_solids())
			else:
				solids = comparePGE(self.pGEs, A_G_V.get_solids(2))
			for obj in A_G_V.gameSprites["objects"]:
				if obj.magic:
					solids.append(obj)
			newRect, death = physic_collision(move_vector, self.rect, solids, hazards)
			if death:
				A_G_V.loose()
			deplaced = distancePoint(self.rect.center, newRect.center)
			self.rect = newRect

		if res.get_cheat(5):
			self.rect = movedPlayer

		exitRect = pygame.Rect(0, 0, 40, 40)
		exitRect.center = A_G_V.gameSprites["exitPos"]
		if collideCircle(self.rect, exitRect) and not self.noColl:
			A_G_V.win()

		for hazard in comparePGE(self.pGEs, A_G_V.gameSprites["hazardProjectiles"]):
			if collideCircle(self.rect, hazard.hitbox) and not self.noColl:
				hazard.kill()
				A_G_V.loose()

		self.cCAngle = get_angle(self.rect.center, A_G_V.mousePos)

		res.stats["distanceTraveled"] += deplaced
		if deplaced < 5:
			self.skin = int(deplaced)
		else:
			self.skin = 5
			A_G_V.gameSprites["particles"].add(1, 10, self.rect.center, (255, 255, 255), 200, 5, 1)

		if self.freeze or not self.outStart:
			self.skin = 6

		if self.focusObj is None:
			self.sDAngle = limitangle(self.sDAngle+self.sDRotate)
		else:
			if self.focusObj.alive():
				self.sDAngle = get_angle(self.rect.center, self.focusObj.rect.center)
			else:
				self.unFocus()

		if self.shootCoolDown <= 0 and not self.noColl and self.outStart:
			if self.shooting == 1:
				res.stats["projShooted"] += 1
				res.soundMananger.playSound("shoot1")
				if res.get_cheat(4):
					for i in range(0,16,2):
						A_G_V.addProj(projectile(self.rect.center, self.sDAngle+i-10, projectile_models["whiteArrow"]))
				else:
					proj = projectile(self.rect.center, self.sDAngle, projectile_models["whiteArrow"])
					A_G_V.addProj(proj)
				self.shootCoolDown = 20
				if res.get_cheat(3):
					self.shootCoolDown = 5
			elif self.shooting == 2:
				res.stats["projShooted"] += 1
				res.soundMananger.playSound("shoot2")
				randangle = spreadAngle(self.sDAngle, 7)
				if res.get_cheat(4):
					for i in range(0,16,2):
						A_G_V.addProj(projectile(self.rect.center, randangle+i-10, projectile_models["blueFragment"]))
				else:
					proj = projectile(self.rect.center, randangle, projectile_models["blueFragment"])
					proj.pos[0] += proj.motion[0]
					proj.pos[1] += proj.motion[1]
					A_G_V.addProj(proj)
				self.shootCoolDown = 5
				if res.get_cheat(3):
					self.shootCoolDown = 1
		else:
			self.shootCoolDown -= 1

		if self.shieldTime > 0:
			self.shieldTime -= 1
			if self.shieldTime == 1:
				self.speed = 1

	def shoot(self, button):

		self.shooting = button

	def unShoot(self, button=0):

		if button == 0:
			self.shooting = 0
		elif self.shooting == button:
			self.shooting = 0

	def focusBlock(self, focusList):

		if self.focusObj in focusList:
			focusList.remove(self.focusObj)
		self.unFocus()
		if len(focusList) > 0:
			angleList = []
			for obj in focusList:
				angle = get_angle(self.rect.center, obj.rect.center)
				if self.sDAngle > 180 and angle < limitangle(self.sDAngle+180):
					angle += 360
				elif self.sDAngle <= 180 and angle > limitangle(self.sDAngle+180):
					angle -= 360
				angle = self.sDAngle-angle
				if math.fabs(angle) < 23:
					angleList.append([angle, obj])
			angleList.sort(key=lambda a: math.fabs(a[0])+distancePoint(a[1].rect.center, self.rect.center)/50-(a[1].rect.width+a[1].rect.height)/20)
			if len(angleList) > 0:
				self.focusObj = angleList[0][1]
				self.focusObj.focused()

	def focusBlockDes(self):

		if self.lastHit is not None:
			self.unFocus()
			self.focusObj = self.lastHit
			self.focusObj.focused()

	def blockHit(self, obj):

		if obj.hardness > -1:
			self.lastHit = obj

	def rotate(self, way):

		self.unFocus()
		if way == 1:
			self.sDRotate = 5
		elif way == 2:
			self.sDRotate = -5

	def unRotate(self, way=0):

		if way == 0:
			self.sDRotate = 0
		elif way == 1 and self.sDRotate > 0:
			self.sDRotate = 0
		elif way == 2 and self.sDRotate < 0:
			self.sDRotate = 0

	def unFocus(self):

		if self.focusObj is not None:
			self.focusObj.unFocused()
			self.focusObj = None

	def draw(self, window):

		if not self.noColl:
			if self.shield:
				self.imgShield.draw(window, self.rect.center)
			rotatedCC = pygame.transform.rotate(self.cursorCircle, self.cCAngle)
			if self.focusObj is not None:
				draw_dotted_line(window, self.rect.center, self.focusObj.rect.center, self.miniCount)
			window.blit(self.skins[self.skin], self.rect.move(-1,-1))
			if self.showCursor:
				rotatedSD = pygame.transform.rotate(self.shootDirection, self.sDAngle)
				window.blit(rotatedSD, rotatedSD.get_rect(center=self.rect.center))
			if self.freeze == False:
				if self.mouseDistance < 40:
					opacity = 0
				elif self.mouseDistance < 300:
					opacity = self.mouseDistance-40/300*235+20
				else:
					opacity = self.mouseDistance = 255
				blit_alpha(window, rotatedCC, rotatedCC.get_rect(center=self.rect.center), opacity)
			else:
				pygame.draw.circle(window, (255, 255, 255), self.rect.center, 30, 2)
			if self.shieldTime > 0:
				if self.shieldTime%3 == 0:
					window.blit(res.images["player"][7], self.rect.move(-1, -1))

	def hurt(self):

		if not self.noColl and self.outStart:
			if self.shield or self.shieldTime > 0:
				self.shield = False
				if self.shieldTime == 0:
					self.shieldTime = 35
					res.stats["shieldsDestroyed"] += 1
					res.soundMananger.playSound("shieldLoss")
					self.speed *= 0.4
					return 2
				return True
			return False
		return True

	def tp(self, x, y):

		self.unFocus()
		self.rect.center = (x, y)
		res.stats["distanceTraveled"] += (x+y)/2

	def insens(self):

		self.freeze = True
		self.noColl = True

	def uninsens(self):

		self.freeze = False
		self.noColl = False
