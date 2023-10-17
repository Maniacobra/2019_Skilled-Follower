# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import randint, choice
from math import ceil, radians, fabs
from copy import copy

import game_values as GAMEVALUES
from fct import *
import res

class tempEffect(pygame.sprite.Sprite):

	def __init__(self, particle, frames, pos):

		pygame.sprite.Sprite.__init__(self)
		self.phases = {}
		self.image = res.images[particle][0]
		self.rect = self.image.get_rect(center=pos)
		self.frame = 0
		self.end = frames
		sequences = frames/len(res.images[particle])
		imageFrame = 0
		for phase in range(0, len(res.images[particle])):
			self.phases[imageFrame] = res.images[particle][phase]
			imageFrame += sequences

	def update(self):

		for phase in self.phases.items():
			if self.frame >= phase[0]:
				self.image = phase[1]
		self.frame += 1
		if self.frame >= self.end:
			self.kill()

class whiteSquare(pygame.sprite.Sprite):

	def __init__(self, rect):

		pygame.sprite.Sprite.__init__(self)
		self.rect = rect
		self.fixedPos = self.rect.center
		self.image = pygame.Surface((self.rect.width, self.rect.height))

	def update(self):

		self.rect = self.rect.inflate(-6, -6)
		self.rect.center = self.fixedPos
		self.image = pygame.Surface((self.rect.width, self.rect.height))
		self.image.fill((255, 255, 255))
		if self.rect.width <= 6 or self.rect.height <= 6:
			self.kill()

class whiteCircle(pygame.sprite.Sprite):

	def __init__(self, rect):

		pygame.sprite.Sprite.__init__(self)
		self.rect = rect
		self.radius = int(self.rect.w/2)
		self.image = pygame.Surface((self.rect.width, self.rect.height))
		self.image.set_colorkey((0, 0, 0))
		pygame.draw.circle(self.image, (255, 255, 255), (int(self.rect.w/2), int(self.rect.h/2)), self.radius)

	def update(self):

		self.radius -= 3
		self.image = pygame.Surface((self.rect.width, self.rect.height))
		self.image.set_colorkey((0, 0, 0))
		pygame.draw.circle(self.image, (255, 255, 255), (int(self.rect.w/2), int(self.rect.h/2)), self.radius)
		if self.radius <= 3:
			self.kill()

class growingCircle(pygame.sprite.Sprite):

	def __init__(self, pos, size, speed, color=(255, 255, 255)):

		pygame.sprite.Sprite.__init__(self)
		self.circle = 5
		self.size = size
		self.grow = (speed/100)*(size/2-5)
		self.image = pygame.Surface((self.size+10, self.size+10), SRCALPHA)
		self.rect = self.image.get_rect(center=pos)
		self.color = color

	def update(self):

		self.circle += self.grow
		if self.circle < self.size/2:
			width = 6
			if self.circle > self.size/2-5:
				width = 1
			elif self.circle > self.size/2-15:
				width = 3
			elif self.circle > self.size/2-25:
				width = 4
			elif self.circle > self.size/2-40:
				width = 5
			if width > self.circle:
				width = 0
			self.image = pygame.Surface((self.size+10, self.size+10), SRCALPHA)
			pygame.draw.circle(self.image, self.color, (int(self.size/2), int(self.size/2)), int(self.circle), width)
		else:
			self.kill()

class particleLayer:

	def __init__(self, max, pFU):

		self.max = max
		self.particles = []
		self.speed = pFU

	def update(self):

		self.anim = self.speed
		for particle in self.particles:
			particle.update()
			if particle.alpha <= 25:
				self.particles.remove(particle)

	def draw(self, window):

		img = pygame.Surface((res.settings["PART_SIZE"], res.settings["PART_SIZE"]))
		for particle in self.particles:
			img.set_alpha(particle.alpha)
			img.fill(particle.color)
			window.blit(img, particle.rect)

	def add(self, *partArgs):

		partSize = len(self.particles)
		for i in range(0, ceil(partArgs[0]/self.speed*res.settings["PART_NB_MULT"])):
			if partSize < self.max:
				particle = framePixel(*partArgs[1:], self.speed)
				self.particles.append(particle)

	def reset(self, max, pFU):

		self.max = max
		self.pFU = pFU
		if len(self.particles) > self.max:
			self.particles = []

class framePixel:

	def __init__(self, frame, pos, color, opacity, disp, dep, speed):

		self.speed = speed
		self.pos = pos[0]+randint(-disp, disp), pos[1]+randint(-disp, disp)
		self.rect = pygame.Rect(self.pos[0]-res.settings["PART_SIZE"]/2, self.pos[1]-res.settings["PART_SIZE"]/2, res.settings["PART_SIZE"], res.settings["PART_SIZE"])
		self.motion = randFloat(-dep, dep)*self.speed, randFloat(-dep, dep)*self.speed
		frame = frame/self.speed
		self.alpha = opacity
		self.color = color
		self.alphaReduction = self.alpha/frame
		self.updateWait = 0

	def update(self):

		if self.updateWait <= 0:
			self.updateWait = self.speed
			self.pos = self.pos[0]+self.motion[0], self.pos[1]+self.motion[1]
			self.rect.center = self.pos
			self.alpha -= self.alphaReduction
		self.updateWait -= 1

	def set_speed(self, speed):

		self.motion = self.motion[0]*speed, self.motion[1]*speed
		self.frame *= speed
		self.alphaReduction *= speed

class flash(pygame.sprite.Sprite):

	def __init__(self, color=(255, 255, 255), opacity=255, frame=15):

		pygame.sprite.Sprite.__init__(self)
		self.frame = frame
		self.rect = pygame.Rect(0, 0, 1366, 768)
		self.image = pygame.Surface((1366, 768))
		self.image.fill(color)
		self.image.set_alpha(opacity)
		self.alpha = opacity
		self.alphaReduction = self.alpha/frame

	def update(self):

		if self.frame <= 0:
			self.kill()
		self.frame -= 1
		self.alpha -= self.alphaReduction
		self.image.set_alpha(self.alpha)

class fade(pygame.sprite.Sprite):

	def __init__(self, color=(255, 255, 255), opacity=255, frame=15):

		pygame.sprite.Sprite.__init__(self)
		self.frame = frame
		self.rect = pygame.Rect(0, 0, 1366, 768)
		self.image = pygame.Surface((1366, 768))
		self.image.fill(color)
		self.image.set_alpha(0)
		self.alpha = 0
		self.alphaAddition = opacity/frame

	def update(self):

		if self.frame <= 0:
			self.kill()
		self.frame -= 1
		self.alpha += self.alphaAddition
		self.image.set_alpha(self.alpha)

class rotativeDeco:

	def __init__(self, image):

		self.image = image
		self.rot = randint(3, 7)
		self.angle = 0
		if randint(0, 1) == 0:
			self.rot *= -1

	def draw(self, window, pos):

		window.blit(rot_center(self.image, self.angle), self.image.get_rect(center=pos))
		self.angle += self.rot

class falling_beam:

	def __init__(self):

		r = randint(0, 255)
		if r < 255:
			v = randint(0, 255-r)
		else:
			v = 0
		self.color = (r, v, 255-r-v)
		self.speed = randint(5, 15)
		self.pos = [randint(0, 1366), 0]

	def update(self):

		self.pos[1] += self.speed
		if self.pos[1] >= 768+self.speed*22:
			self.speed = 0

	def draw(self, window):

		pygame.draw.line(window, [int(c*0.3) for c in self.color], (self.pos[0], self.pos[1]-self.speed*22), self.pos, 1)
		pygame.draw.line(window, [int(c*0.65) for c in self.color], (self.pos[0], self.pos[1]-self.speed*15), self.pos, 1)
		pygame.draw.line(window, self.color, (self.pos[0], self.pos[1]-self.speed*5), self.pos, 3)
		pygame.draw.line(window, self.color, (self.pos[0], self.pos[1]-self.speed*10), self.pos, 1)

class animated_bg:

	def __init__(self):

		self.bg1 = 0
		self.bg2 = -768
		self.objects = []
		self.speed = 20
		self.count = 1
		self.objList = ["exit", "spikes", "largeWall", "glassBlock", "smallSquare", "wood_block", "pylone", "wood_cone", "glass_cone", "turret", "laz_turret", "laz_square", "circularSaw", "spike_square", "smallWall", "spike_wall", "a-ring", "teleporter", "spiky_wood", "spiky_wheel"]
		self.objList *= 2
		self.objList += ["start", "exit_close", "tesla", "square_button", "turret"]

	def update(self):

		if res.settings["MOVING_BG"]:
			self.bg1 += 2
			self.bg2 += 2
			if self.bg1 >= 768:
				self.bg1 = -768
			elif self.bg2 >= 768:
				self.bg2 = -768
			self.count -= 1
			if self.count == 0:
				self.count = 25
				name = choice(self.objList)
				if name in ("largeWall", "smallWall"):
					tex = 3
				elif name == "spike_wall":
					tex = 2
				else:
					tex = randint(0, len(res.images[name])-1)
				x = randint(50, 1266)
				if len(self.objects) > 0:
					while fabs(self.objects[-1][0][0]-x) < 100:
						x = randint(50, 1266)
				self.objects.append([[x, -50], name, tex, choice([0, 90, 180, 270])])
				if name == "turret":
					attName = "cannon"
					if randint(0, 5) == 1 and tex < 5:
						attName = "cannon_double"
					self.objects.append([[x, -50], attName, tex, randint(0, 360)])
				elif name == "laz_turret":
					self.objects.append([[x, -50], "lazer", tex, randint(0, 360)])
			for obj in self.objects:
				obj[0][1] += 2
				if obj[0][1] > 868:
					self.objects.remove(obj)

	def draw(self, window):

		if not res.settings["MOVING_BG"]:
			window.blit(res.images["bg"][0], (0, 0))
		else:
			window.blit(res.images["bg"][1], (0, self.bg1))
			window.blit(res.images["bg"][1], (0, self.bg2))
			for obj in self.objects:
				if obj[1] == "exit":
					obj[2] += 0.2
					if obj[2] >= 4:
						obj[2] = 0
				elif obj[1] == "a-ring":
					obj[2] += 0.1
					if obj[2] >= 3:
						obj[2] = 0
				elif obj[1] == "circularSaw":
					obj[3] += 10
					obj[3] = limitangle(obj[3])
				elif obj[1] in ("teleporter", "cannon_double", "spiky_wheel"):
					obj[3] -= 7
					obj[3] = limitangle(obj[3])

				img = pygame.transform.rotate(res.images[obj[1]][int(obj[2])], obj[3])

				window.blit(img, img.get_rect(center=obj[0]))

def draw_cornerBar(rect, h, d):

	image = pygame.Surface(rect.size, pygame.SRCALPHA)
	barx = d/h*(rect.width/2)+1
	bary = d/h*(rect.height/2)+1
	tl_w = pygame.Rect(0, 0, barx, 5)
	tl_h = pygame.Rect(0, 0, 5, bary)
	tr_w = pygame.Rect(rect.width-barx, 0, barx, 5)
	tr_h = pygame.Rect(rect.width-5, 0, 5, bary)
	bl_w = pygame.Rect(0, rect.height-5, barx, 5)
	bl_h = pygame.Rect(0, rect.height-bary, 5, bary)
	br_w = pygame.Rect(rect.width-barx, rect.height-5, barx, 5)
	br_h = pygame.Rect(rect.width-5, rect.height-bary, 5, bary)
	rects = tl_w, tl_h, tr_w, tr_h, bl_w, bl_h, br_w, br_h
	for r in rects:
		pygame.draw.rect(image, (255, 255, 255), r)
	return image

def draw_circleBar(rect, h, d, angle):

	image = pygame.Surface(rect.size, pygame.SRCALPHA)
	end_angle = radians(d/h*360)
	angle = radians(angle)
	pygame.draw.arc(image, (255, 255, 255), image.get_rect(), angle, end_angle+angle, 5)
	return image

def draw_range_rect(rect, angle, range):

	image = pygame.Surface(rect.size, SRCALPHA)
	vect = get_vect(angle+range, rect.height)
	endpos = rect.width/2+vect[0], rect.height/2+vect[1]
	pygame.draw.line(image, (0, 0, 0), (rect.width/2, rect.height/2), endpos, 12)
	pygame.draw.line(image, (150, 150, 150), (rect.width/2, rect.height/2), endpos, 6)
	vect = get_vect(angle-range, rect.height)
	endpos = rect.width/2+vect[0], rect.height/2+vect[1]
	pygame.draw.line(image, (0, 0, 0), (rect.width/2, rect.height/2), endpos, 12)
	pygame.draw.line(image, (150, 150, 150), (rect.width/2, rect.height/2), endpos, 6)
	pygame.draw.rect(image, (0, 0, 0), (0, 0, rect.width, rect.height), 4)
	return image

def draw_range_circle(rect, angle, range):

	image = pygame.Surface(rect.size, SRCALPHA)
	center = rect.height/2
	vect = get_vect(angle+range, center-5)
	endpos = center+vect[0], center+vect[1]
	pygame.draw.line(image, (0, 0, 0), (center, center), endpos, 10)
	pygame.draw.line(image, (150, 150, 150), (center, center), endpos, 4)
	vect = get_vect(angle-range, center-5)
	endpos = center+vect[0], center+vect[1]
	pygame.draw.line(image, (0, 0, 0), (center, center), endpos, 10)
	pygame.draw.line(image, (150, 150, 150), (center, center), endpos, 4)
	return image

def draw_electricStrike(window, pos1, pos2, var=8):

	origin = list(pos1)
	oldPoint = origin
	for vect in vectCutting(pos1[0]-pos2[0], pos1[1]-pos2[1], var):
		origin[0] -= vect[0]
		origin[1] -= vect[1]
		newPoint = origin[0]+randint(0, var*2)-var, origin[1]+randint(0, var*2)-var
		pygame.draw.line(window, (200, 220, 255), oldPoint, newPoint, 2)
		oldPoint = newPoint
	pygame.draw.line(window, (200, 220, 255), oldPoint, pos2, 2)

def draw_select_area(window, rect, time, shape, color=(255, 255, 255), tick=1):

	infl = time-30
	if infl <= 0:
		infl += 30
	if shape == 0:
		pygame.draw.rect(window, color, rect.inflate(infl, infl), tick)
	else:
		pygame.draw.circle(window, color, rect.center, int((rect.width+infl)/2), tick)

def draw_dotted_line(window, pos1, pos2, time):

	newPoint = list(pos1)
	i = 0
	for vect in vectCutting(pos1[0]-pos2[0], pos1[1]-pos2[1], 1):
		newPoint[0] -= vect[0]
		newPoint[1] -= vect[1]
		if i%20 == time:
			pygame.draw.line(window, (180, 210, 255), newPoint, (newPoint[0]+vect[0]*2, newPoint[1]+vect[1]*2), 2)
		i += 1
