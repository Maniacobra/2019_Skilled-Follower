# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random
import math

import game_values as GAMEVALUES
from proj_models import projectile_models
from visuals import *
from fct import *
from projectile import *
import res
from speObj_instance import instance

class tp(instance):

    def __init__(self, obj, param, scoreMlt):

        self.startpos = obj.rect.center
        self.endpos = param["pos"][0]
        self.singleUse = param["sUse"]
        self.travel = 0
        self.activeTp = False
        self.travelPos = self.startpos
        self.angle = get_angle(self.startpos, self.endpos)
        self.plTp_img = pygame.transform.rotate(res.images["plTp"][0], self.angle)
        self.cursorImg = pygame.transform.rotate(res.images["tpCursor"][0], self.angle)
        self.cd = 0

    def update(self, obj, A_G_V):

        if self.cd > 0:
            self.cd -= 1
        if not A_G_V.gameSprites["player"].noColl and obj.collide(A_G_V.gameSprites["player"].rect) and not obj.delete and not self.activeTp and self.cd == 0:
            self.cd = 360
            self.activeTp = True
            A_G_V.gameSprites["player"].insens()
            res.soundMananger.playSound("tpEnter")

        if self.activeTp:
            A_G_V.gameSprites["player"].insens()
            self.travel += 20
            vect = get_vect(self.angle, self.travel)
            A_G_V.gameSprites["player"].tp(self.startpos[0]+vect[0], self.startpos[1]+vect[1])
            self.travelPos = A_G_V.gameSprites["player"].rect.center
            if self.travel >= distancePoint(self.startpos, self.endpos):
                A_G_V.gameSprites["player"].tp(*self.endpos)
                self.activeTp = False
                self.travel = 0
                A_G_V.gameSprites["player"].uninsens()
                res.soundMananger.playSound("tpExit")
                A_G_V.gameSprites["particles"].add(50, 50, A_G_V.gameSprites["player"].rect.center, (190, 255, 255), 255, 1, 2)
                A_G_V.gameSprites["visuals"].add(growingCircle(A_G_V.gameSprites["player"].rect.center, 120, 4))
                A_G_V.gameSprites["player"].shieldTime = 40
                A_G_V.gameSprites["player"].speed *= 0.2
                if self.singleUse:
                    obj.delete = True
            A_G_V.gameSprites["particles"].add(3, 100, self.travelPos, (255, 255, 255), 255, 5, 0.7)

        if res.settings["GRAPHS"] > 1 and self.cd == 0:
            A_G_V.gameSprites["particles"].add(3, 30, obj.rect.center, (200, 200, 255), 200, 20, 4)

    def draw(self, window, rect):

        if self.cd == 0:
            window.blit(self.cursorImg, self.cursorImg.get_rect(center=rect.center))

    def fdraw(self, window, rect):

        if self.activeTp:
            plTp_rect = self.plTp_img.get_rect(center=self.travelPos)
            window.blit(self.plTp_img, plTp_rect)

class moving(instance):

    def __init__(self, obj, param, scoreMlt):

        self.speed = param["s"]
        self.posList = param["pos"]
        if len(self.posList) == 1:
            self.posList.append(obj.rect.center)
        self.travel = param["start"]
        self.active = param["active"]
        self.pauses = param["p1"], param["p2"], param["p3"], param["p4"], param["p5"]
        if type(self.speed) == float:
            perimeter = 0
            prevPos = self.posList[0]
            for pos in self.posList[1:]:
                perimeter += distancePoint(pos, prevPos)
                prevPos = pos
            self.speed = perimeter/(self.speed*60)
        else:
            self.speed *= ((1+scoreMlt)/2)
        self.currentPos = list(obj.rect.center)

    def update(self, obj, A_G_V):

        if self.active:
            nextpoint = self.posList[self.travel]
            if distancePoint(obj.fixedRect.center, nextpoint) <= self.speed:
                obj.fixedRect.center = nextpoint
                obj.rect.center = nextpoint
                obj.hitbox.center = nextpoint
                self.travel += 1
                if self.travel > len(self.posList)-1:
                    self.travel = 0
                if self.travel in self.pauses:
                    self.active = False
            else:
                vect = get_vect(get_angle(obj.fixedRect.center, nextpoint), self.speed)
                self.currentPos[0] += vect[0]
                self.currentPos[1] += vect[1]
                obj.rect.center = self.currentPos
                obj.fixedRect.center = self.currentPos
                obj.hitbox.center = self.currentPos
            obj.set_pGE()

    def signal(self, signal, obj):

        if signal == "moveStop":
            self.active = False
        elif signal == "moveStart":
            self.active = True
        elif signal[:12] == "movingChangeSpeed-":
            self.speed = int(signal[12:])

class orbit(instance):

    def __init__(self, obj, param, scoreMlt):

        self.center = param["cen"][0]
        self.speed = (param["s"]/10)*((1+scoreMlt)/2)
        self.active = param["active"]
        self.angle = get_angle(self.center, obj.fixedRect.center)
        self.radius = distancePoint(self.center, obj.fixedRect.center)

    def update(self, obj, A_G_V):

        if self.active:
            self.angle += self.speed
            self.angle = limitangle(self.angle)
            vect = get_vect(self.angle, self.radius)
            newPos = self.center[0]+vect[0], self.center[1]+vect[1]
            obj.rect.center = newPos
            obj.fixedRect.center = newPos
            obj.hitbox.center = newPos
            obj.set_pGE()

    def signal(self, signal, obj):

        if signal == "orbitStop":
            self.active = False
        elif signal == "orbitStart":
            self.active = True
        elif signal[:12] == "moveChangeSpeed-":
            self.speed = int(signal[12:])

class forceField(instance):

    def __init__(self, obj, param, scoreMlt):

        obj.magic = obj.texture != 2
        self.repulse = False
        self.flashTime = 0
        self.mustClose = False

    def update(self, obj, A_G_V):

        if obj.texture != 2:
            if obj.collided and not self.repulse:
                self.repulse = True
                obj.update_img(1)
            elif not obj.collided and self.repulse:
                self.repulse = False
                obj.update_img(0)
        if self.flashTime > 0:
            self.flashTime -= 1
            if self.mustClose:
                if self.flashTime == 0:
                    obj.magic = True
                    obj.update_img(0)
                    if obj.collide(A_G_V.gameSprites["player"].rect):
                        A_G_V.loose()

    def signal(self, signal, obj):

        if signal == "wallOpen" and obj.texture != 2:
            res.soundMananger.playSound("magicWall_open")
            obj.update_img(2)
            self.flashTime = 5
            obj.magic = False
            self.mustClose = False

        elif signal == "wallClose" and obj.texture == 2:
            res.soundMananger.playSound("magicWall_close")
            self.flashTime = 5
            self.mustClose = True

    def sdraw(self, window, rect):

        if self.flashTime > 0:
            window.fill((255, 255, 255), rect)

class followMove(instance):

    def __init__(self, obj, param, scoreMlt):

        self.f = False
        self.targetID = param["tar"]
        self.target = None
        self.lastPos = obj.fixedRect.center

    def firstAction(self, obj, A_G_V):

        for s_obj in A_G_V.gameSprites["objects"]:
            if s_obj.id == self.targetID:
                self.target = s_obj
                self.lastPos = self.target.fixedRect.center

    def update(self, obj, A_G_V):

        if not self.f:
            self.f = True
            self.firstAction(obj, A_G_V)
        elif self.target is not None:
            if self.target.fixedRect.center != self.lastPos:
                newPos = obj.fixedRect.centerx+(self.target.fixedRect.centerx-self.lastPos[0]), obj.fixedRect.centery+(self.target.fixedRect.centery-self.lastPos[1])
                self.lastPos = self.target.fixedRect.center
                obj.rect.center = newPos
                obj.fixedRect.center = newPos
                obj.hitbox.center = newPos
                obj.set_pGE()

class point(instance):

    def __init__(self, obj, param, scoreMlt):

        self.anim_count = random.randrange(0, 100)
        self.move_increasment = 0

    def update(self, obj, A_G_V):

        if distancePoint(obj.rect.center, A_G_V.gameSprites["player"].rect.center) < 30:
            res.soundMananger.playSound("collect")
            obj.kill()
            A_G_V.points(GAMEVALUES.ringPts)
        elif distancePoint(obj.rect.center, A_G_V.gameSprites["player"].rect.center) < 70:
            self.move_increasment += 0.25
            obj.rect = obj.rect.move(get_vect(get_angle(obj.rect.center, A_G_V.gameSprites["player"].rect.center), 6+self.move_increasment))
        else:
            self.move_increasment = 0
        self.anim_count += 1
        if self.anim_count == 100:
            self.anim_count = 0
            obj.update_img(0)
        elif self.anim_count == 90:
            obj.update_img(1)
        elif self.anim_count == 80:
            obj.update_img(2)
        elif self.anim_count == 70:
            obj.update_img(1)
