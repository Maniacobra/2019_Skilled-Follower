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

class megaShoot(instance):

    def __init__(self, obj, shootConfig, scoreMlt):

        self.proj = shootConfig["p"]
        self.inter = int(shootConfig["cd"]*(1/((2+scoreMlt)/3)))
        self.nb = shootConfig["nb"]
        self.cooldown = 5
        self.waitSignal = False
        if self.inter < 0:
            self.inter = -1
            self.waitSignal = True


    def update(self, obj, A_G_V):

            if A_G_V.end is None and A_G_V.unlock and not self.waitSignal:
                if not self.waitSignal and self.inter == -1:
                    self.waitSignal = True
                    self.cooldown = 0
                if self.cooldown <= 0:
                    self.cooldown = self.inter
                    ran = randint(0, self.nb)
                    for angle in range(0+ran, 360+ran, self.nb):
                        vect = get_vect(angle, obj.rect.w/2+projectile_models[self.proj]["r"]/2+3)
                        pos = obj.rect.center[0]+vect[0]+1, obj.rect.center[1]+vect[1]+1
                        proj = projectile(pos, angle, projectile_models[self.proj])
                        A_G_V.addProj(proj, True)
                    A_G_V.gameSprites["visuals"].add(whiteCircle(obj.rect.inflate(80, 80)))
                    A_G_V.gameSprites["visuals"].add(growingCircle(obj.rect.move(5, 5).center, 200, 3))
                    res.soundMananger.playSound("impulse")
                else:
                    self.cooldown -= 1

    def signal(self, signal, obj):

        if signal == "shoot":
            self.waitSignal = False

class lazer(instance):

    def __init__(self, obj, param, scoreMlt):

        self.angle = obj.angle
        self.speed = param["s"]/10
        self.range = param["r"]/2
        self.mode = param["m"]
        self.squared = param["sq"]
        self.on = param["on"]
        self.rot = param["rot"]
        self.reaction = False
        if self.mode == 0:
            self.color = (255, 50, 50)
        elif self.mode == 1:
            self.color = (85, 90, 255)
        else:
            self.color = (50, 255, 50)
        if self.squared:
            self.startpoint = obj.rect.move(get_vect(self.angle, obj.rect.height/2)).center
        else:
            self.startpoint = obj.rect.move(get_vect(self.angle, 70)).center
        self.endpoint = self.startpoint
        self.image = pygame.transform.rotate(res.images["lazer"][obj.texture], self.angle)
        self.rect = self.image.get_rect(center=obj.rect.center)
        if self.range < 360:
            if obj.shape == 0:
                self.deco = draw_range_rect(obj.rect, obj.angle, self.range)
            else:
                self.deco = draw_range_circle(obj.rect, obj.angle, self.range)

    def update(self, obj, A_G_V):

        if self.reaction:
            self.reaction = False

        angle = self.angle
        updateAngle = True
        if self.rot == 1:
            angle += self.speed
        elif self.rot == 2:
            angle = get_angle(obj.rect.center, A_G_V.gameSprites["player"].rect.center)
        angle = limitangle(angle)
        self.rect = self.image.get_rect(center=obj.rect.center)
        if self.range < 180 and not self.squared:
            limit1 = limitangle(obj.angle-self.range)
            limit2 = limitangle(obj.angle+self.range)
            limit1, limit2 = limit2, limit1
            if not(angle<limit1 or angle>limit2):
                if self.rot < 2:
                    self.speed *= -1
                else:
                    updateAngle = False
        if updateAngle:
            self.angle = angle
            self.image = pygame.transform.rotate(res.images["lazer"][obj.texture], self.angle)

        if self.on:
            res.soundMananger.hold_loop("lazer", 100/distancePoint(A_G_V.gameSprites["player"].rect.center, obj.rect.center))
            if self.squared:
                self.startpoint = obj.rect.move(get_vect(self.angle, obj.rect.height/2)).center
            else:
                self.startpoint = obj.rect.center
            self.endpoint = obj.rect.move(get_vect(self.angle, 1525)).center

            solid_rects = [obj.hitbox.inflate(2, 2) for obj in A_G_V.get_solids() if obj.shape == 0]
            circles = [(obj.hitbox.centerx, obj.hitbox.centery, obj.hitbox.w/2+2) for obj in A_G_V.get_solids(True) if obj.shape == 1]
            if A_G_V.end is None:
                circles.append((*A_G_V.gameSprites["player"].rect.center, 11))
            result = raycast(solid_rects, circles, self.startpoint, self.endpoint)

            if result is not None:
                vect = get_vect(self.angle, 1525*result)
                self.endpoint = self.startpoint[0]+vect[0], self.startpoint[1]+vect[1]

            if not self.mode == 1:
                if distancePoint(self.endpoint, A_G_V.gameSprites["player"].rect.center) < 14:
                    A_G_V.loose()
            if not self.mode == 0:
                for proj in [proj for proj in A_G_V.gameSprites["projectiles"] if proj.damages > 0]:
                    if raycast_circle((*proj.hitbox.center, proj.hitbox.height+self.speed*5+proj.speed-5), self.startpoint, self.endpoint) is not None:
                        proj.delete = True
            if not self.squared:
                decal = get_vect(get_angle(self.startpoint, self.endpoint), 70)
                self.startpoint = list(self.startpoint)
                self.startpoint[0] += decal[0]
                self.startpoint[1] += decal[1]
            A_G_V.gameSprites["particles"].add(3, 15, self.endpoint, self.color, 255, 1, 2)
            vect = self.endpoint[0]-self.startpoint[0], self.endpoint[1]-self.startpoint[1]
            p_pos = self.startpoint
            for pos in vectCutting(*vect, 10):
                p_pos = p_pos[0]+pos[0], p_pos[1]+pos[1]
                prob = int(5*(1/res.settings["PART_NB_MULT"]))
                if prob < 4:
                    prob = 4
                if random.randrange(0, prob) == 0:
                    A_G_V.gameSprites["particles"].add(1, 10, p_pos, self.color, 255, 1, 1)

    def draw(self, window, rect):

        if self.range < 180:
            window.blit(self.deco, rect)

    def fdraw(self, window, rect):

        if self.on and not self.reaction:
            pygame.draw.line(window, self.color, self.startpoint, self.endpoint, 3)
        if not self.squared:
            window.blit(self.image, self.rect)

    def signal(self, signal, obj):

        if signal == "lazerOn":
            self.on = True
            self.reaction = True
        elif signal == "lazerOff":
            self.on = False
        elif signal == "lazerRot":
            self.rot = True
        elif signal == "lazerRotStop":
            self.rot = False

class tesla(instance):

    def __init__(self, obj, param, scoreMlt):

        self.scope = param["scope"]
        self.on = param["on"]
        self.warning = 1
        self.load = 1/param["load"]
        self.playerPos = 0, 0
        self.active = True

    def update(self, obj, A_G_V):

        self.playerPos = A_G_V.gameSprites["player"].rect.center
        if distancePoint(A_G_V.gameSprites["player"].rect.center, obj.rect.center) <= self.scope and self.active and A_G_V.end is None and self.on and A_G_V.gameSprites["player"].outStart:
            if self.warning <= 0:
                res.soundMananger.playSound("electric_strike")
                if A_G_V.loose():
                    self.active = False
            else:
                self.warning -= self.load
        elif self.warning < 1:
            self.warning += self.load*2
            if self.warning > 1:
                self.warning = 1

    def fdraw(self, window, rect):

        if self.on:
            if self.warning < 1:
                pygame.draw.circle(window, (255, 100, 100), rect.center, self.scope, 1)
            if int(self.scope*self.warning) > 10:
                pygame.draw.circle(window, (255, 255, 255), rect.center, int(self.scope*self.warning), 1)
            if self.warning <= 0.05 and self.active:
                draw_electricStrike(window, rect.center, self.playerPos)
                pygame.draw.circle(window, (255, 255, 255), rect.center, 10)

    def signal(self, obj, signal):

        if signal == "teslaOn":
            self.on = True
        elif signal == "teslaOff":
            self.on = False
