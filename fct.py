# -*- coding: utf-8 -*-

from time import sleep
import pygame
import random
import math
import pickle
from itertools import chain
import pygame

from config import *
import res

def get_vect(angle, speed):

	angle = -math.radians(angle)
	xu = 0
	yu = speed
	xv = math.cos(angle)*xu-math.sin(angle)*yu
	yv = math.sin(angle)*xu+math.cos(angle)*yu
	return [-xv, -yv]

def get_angle(pos1, pos2):

	dy = pos2[1] - pos1[1]
	dx = pos2[0] - pos1[0]
	angle = math.degrees(math.atan2(-dx,  -dy))
	if angle < 0:
		angle = 360+angle
	return angle

def pixelDistancePoint(pos1, pos2):

	disx = math.fabs(pos1[0]-pos2[0])
	disy = math.fabs(pos1[1]-pos2[1])
	return (disx+disy)/2

distancePoint = lambda pos1, pos2 : math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)

spreadAngle = lambda angle, spread : angle+random.randint(-spread, spread)

def vectCutting(x, y, pxRange):

	array = []
	if math.fabs(x) > math.fabs(y):
		for nb in range(0, int(math.fabs(x)), pxRange):
			if x > 0:
				array.append([pxRange, 0])
			else:
				array.append([-pxRange, 0])
		for nb in range(0, int(math.fabs(y)), pxRange):
			if y > 0:
				array[int(nb/y*x/pxRange)][1] = pxRange
			else:
				array[int(nb/y*x/pxRange)][1] = -pxRange
	else:
		for nb in range(0, int(math.fabs(y)), pxRange):
			if y > 0:
				array.append([0, pxRange])
			else:
				array.append([0, -pxRange])
		for nb in range(0, int(math.fabs(x)), pxRange):
			if x > 0:
				array[int(nb/x*y/pxRange)][0] = pxRange
			else:
				array[int(nb/x*y/pxRange)][0] = -pxRange
	for pixels in array:
		yield pixels

randFloat = lambda r1, r2 : random.randint(r1*100, r2*100)/100

def circleRect_collision(rect, r, center):

	circle_distance_x = abs(center[0]-rect.centerx)
	circle_distance_y = abs(center[1]-rect.centery)
	if circle_distance_x > rect.w/2.0+r or circle_distance_y > rect.h/2.0+r:
		return False
	if circle_distance_x <= rect.w/2.0 or circle_distance_y <= rect.h/2.0:
		return True
	corner_x = circle_distance_x-rect.w/2.0
	corner_y = circle_distance_y-rect.h/2.0
	corner_distance_sq = corner_x**2.0 +corner_y**2.0
	return corner_distance_sq <= r**2.0

def collideCircle(r1, r2):

    radii = (r1.w + r2.w) / 2
    squared_distance = (r1.centerx - r2.centerx) ** 2 + (r1.centery - r2.centery) ** 2
    return squared_distance <= radii ** 2

def rot_center(image,  angle):

	try:
		orig_rect = image.get_rect()
		rot_image = pygame.transform.rotate(image,  angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image
	except:
		return image

def lineTexts(str, side, font, pos, distance, color=(255, 255, 255)):

	lines = str.split("!")
	for line in lines:
		text = res.fonts[font].render(line, 1, color)
		if side == 0:
			rect = text.get_rect(topleft=(pos))
		if side == 1:
			rect = text.get_rect(topright=(pos))
		pos[1] += distance
		yield text, rect

def dot(v1,  v2):
    "Dot product of vectors v1 and v2"
    x1,  y1 = v1
    x2,  y2 = v2
    return x1 * x2 + y1 * y2

def raycast_rect(rect,  orig,  dest):

    vertices,  normals = ((rect.bottomleft,  rect.bottomright,  rect.topright,  rect.topleft),
                        ((0,  1),  (1,  0),  (0,  -1),  (-1,  0)))
    lower,  upper = 0.0,  1.0
    x0,  y0 = orig
    x1,  y1 = dest
    ray = (x1-x0,  y1-y0)
    intersection = False

    for vertice,  normal in zip(vertices,  normals):
        orig_to_vertice = (vertice[0]-x0,  vertice[1]-y0)
        n = normal

        numerator = dot(n,  orig_to_vertice)
        denominator = dot(n,  ray)
        if denominator == 0.0:
            if numerator < 0.:
                return None
        else:
            if denominator < 0. and numerator < lower * denominator:
                intersection = True
                lower = numerator / denominator
            elif denominator > 0. and numerator < upper * denominator:
                upper = numerator / denominator

        if upper < lower:
            return None

    if intersection:
        return lower
    return None

def raycast_circle(circle,  orig,  dest):

	x0,  y0 = orig
	x1,  y1 = dest
	h,  k,  r = circle
	a = (x1 - x0)**2 + (y1 - y0)**2
	b = 2 * (x1 - x0) * (x0 - h) + 2 * (y1 - y0) * (y0 - k)
	c = (x0 - h)**2 + (y0 - k)**2 - r**2
	discriminant = b**2 - 4 * a * c
	if discriminant < 0.0:
		return None
	try:
		t = 2 * c / (-b + discriminant**0.5)
	except ZeroDivisionError:
		return None
	if not 0 < t < 1:
		return None
	return t

def raycast(rects,  circles,  orig,  dest):

    fractions_r = (raycast_rect(rect,  orig,  dest) for rect in rects)
    fractions_c = (raycast_circle(circle,  orig,  dest) for circle in circles)
    fraction = min((fraction for fraction in chain(fractions_r,  fractions_c) if fraction is not None),  default=None)

    return fraction

def create_partial_grid(size, xDiv, yDiv):

	xRS = int(size[0]/xDiv)
	yRS = int(size[1]/yDiv)
	partial_grid = {}
	nX, nY = 0, 0
	for x in range(0, size[0]-xRS, xRS):
		nX += 1
		nY = 0
		for y in range(0, size[1]-yRS, yRS):
			nY += 1
			partial_grid[(nX, nY)] = pygame.Rect(x, y, xRS, yRS)
	return (nX, nY), partial_grid

def comparePGE(pGEs, spriteGroup):

	cummonSprites = []
	for num in pGEs:
		for sprite in spriteGroup:
			if num in sprite.pGEs:
				cummonSprites.append(sprite)
	return cummonSprites

def pG_rectLeaving(rect, pG_rect, num):

	mainCase = list(num)
	secondCases = []
	r = rect.w/2
	x = rect.centerx
	y = rect.centery
	diag = 0
	if x+r > pG_rect.right:
		diag = "r"
		if x-r > pG_rect.right:
			mainCase[0] = num[0]+1
		else:
			secondCases.append([num[0]+1, num[1]])
	elif x-r < pG_rect.left:
		diag = "l"
		if x+r < pG_rect.left:
			mainCase[0] = num[0]-1
		else:
			secondCases.append([num[0]-1, num[1]])
	if y+r > pG_rect.bottom:
		if diag == "r":
			secondCases.append([num[0]+1, num[1]+1])
		elif diag == "l":
			secondCases.append([num[0]-1, num[1]+1])
		if y-r > pG_rect.bottom:
			mainCase[1] = num[1]+1
		else:
			secondCases.append([num[0], num[1]+1])
	elif y-r < pG_rect.top:
		if diag == "r":
			secondCases.append([num[0]+1, num[1]-1])
		elif diag == "l":
			secondCases.append([num[0]-1, num[1]-1])
		if y+r < pG_rect.top:
			mainCase[1] = num[1]-1
		else:
			secondCases.append([num[0], num[1]-1])
	secondCases.append(num)
	secondCases = [tuple(num) for num in secondCases]
	return tuple(mainCase), secondCases

def blit_alpha(target,  source,  location,  opacity):

        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(),  source.get_height())).convert()
        temp.blit(target,  (-x,  -y))
        temp.blit(source,  (0,  0))
        temp.set_alpha(opacity)
        target.blit(temp,  location)

def linePoint(p1, p2, percent):

	x = p1[0]+(p2[0]-p1[0])*percent
	y = p1[1]+(p2[1]-p1[1])*percent
	return(x, y)

def espace1(text):

	text = str(text)
	if "1" in text:
		return " 1".join(text.split("1"))
	return text

def insZero(text):

	text = str(text)
	if len(text) < 2:
		return "0"+text
	return text

def convertTime(sec): return "{}h {}m {}s".format(int(sec/3600), insZero(int(sec/60)), insZero(int(sec%60)))

def convertTime2(flt):

	flt = float(flt)
	txt = str(flt.__round__(2))
	txt = txt.split(".")
	sec, mil = txt
	i_sec = int(sec)
	if int(sec) >= 60:
		sec = str(i_sec%60)
		min = str(int(i_sec/60))
	else:
		min = "0"
	if len(min) > 2:
		min = "99"
	return insZero(min)+":"+insZero(sec)+":"+insZero(mil)

def next_value(dict, value, nb=1):

	i = 0
	for k, v in dict.items():
		if v == value:
			keyId = i
			break
		i += 1
	if i+nb > len(dict)-1:
		i = 0
	elif i+nb < 0:
		i = len(dict)-1
	else:
		i += nb
	return dict[list(dict.keys())[i]]

def scalePos(pos): return int(pos[0]/pygame.display.get_surface().get_size()[0]*1366), int(pos[1]/pygame.display.get_surface().get_size()[1]*768)

def orth_angle(angle):

	if angle<90:
		angle = 0
	elif angle<180:
		angle = 90
	elif angle<270:
		angle = 180
	elif angle<360:
		angle = 270

	return angle

def physic_collision(move_vector, rect, solids, dangers):

	death = False
	movedPlayer = rect.move(move_vector)

	for obj in dangers:
		if obj.collide(movedPlayer):
			death = True

	collide = True
	i1 = 0
	while collide:
		collide = False
		for obj in solids:
			if obj.collide(movedPlayer):
				obj.collided = True
				collide = True
				vect = [0, 0]

				if obj.shape == 0:

					dist = (("l", obj.hitbox.left-rect.centerx), ("r", rect.centerx-obj.hitbox.right), \
					("t", obj.hitbox.top-rect.centery), ("b", rect.centery-obj.hitbox.bottom))
					dist = sorted(dist, key=lambda smaller: smaller[1], reverse=True)

					if dist[0][0] == "l":
						vect[0] = -1
						if dist[0][1] == dist[1][1]:
							if dist[1][0] == "t":
								vect[1] = -1
							else:
								vect[1] = 1
					elif dist[0][0] == "r":
						vect[0] = 1
						if dist[0][1] == dist[1][1]:
							if dist[1][0] == "t":
								vect[1] = -1
							else:
								vect[1] = 1
					elif dist[0][0] == "t":
						vect[1] = -1
					elif dist[0][0] == "b":
						vect[1] = 1

				elif obj.shape == 1:
					angle = get_angle(obj.hitbox.center, rect.center)
					if angle < 25 or angle > 335:
						vect = [0, -1]
					elif angle < 65:
						vect = [-1, -1]
					elif angle < 115:
						vect = [-1, 0]
					elif angle < 155:
						vect = [-1, 1]
					elif angle < 205:
						vect = [0, 1]
					elif angle < 245:
						vect = [1, 1]
					elif angle < 315:
						vect = [1, 0]
					elif angle < 335:
						vect = [1, -1]

				i2 = 0
				while obj.collide(movedPlayer):
					movedPlayer = movedPlayer.move(vect)
					i2 += 1
					if i2 > 100:
						return rect, death
		i1 += 1
		if i1 > 5:
			return rect, death

	return movedPlayer, death

def limitangle(angle):

	if angle < 0:
		angle += 360
	elif angle > 360:
		angle -= 360
	return angle

def get_angle_fromVect(vect):

	angle = math.degrees(math.atan(vect[0]/vect[1]))
	if vect[1] > 0:
		angle += 180
	return angle
