# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random
import math

import game_values as GAMEVALUES
from proj_models import projectile_models, proj_group
from visuals import *
from fct import *
from projectile import *
import res
from speObj_instance import instance

class shooting(instance):

    def __init__(self, obj, shootConfig, scoreMlt):

        self.on = True

        self.deco = None
        self.rotRange = math.fabs(shootConfig["r"]/2)
        if self.rotRange < 180:
            if obj.shape == 0:
                self.deco = draw_range_rect(obj.rect, obj.angle, self.rotRange)
            else:
                self.deco = draw_range_circle(obj.rect, obj.angle, self.rotRange)
        else:
            obj.angle = 0
        self.texture = obj.texture
        self.proj = shootConfig["p"]
        self.random = -1
        if self.proj == "RANDOM":
            self.random = 5
            self.proj = random.choice(proj_group)
        self.spread = shootConfig["s"]
        self.inter = int(shootConfig["cd"]*(1/scoreMlt))
        self.onlySignal = False
        if self.inter <= 0:
            self.cooldown = 1
            self.inter = 1
            self.on = False
            self.onlySignal = True
        self.cooldown = random.randint(1, self.inter)
        self.alwaysShoot = shootConfig["alwSh"]
        self.sniperMode = shootConfig["sm"]
        self.angle = int(obj.angle)
        self.shootPos = 0, 0
        self.image = pygame.transform.rotate(res.images["cannon"][self.texture], self.angle)
        self.pos = obj.rect.center
        self.rect = self.image.get_rect(center=self.pos)
        self.activated = False
        self.focusPos = 0, 0

    def update(self, obj, A_G_V):

        if self.random > 0:
            self.random -= 1
            if self.random == 0:
                self.random = 5
                self.proj = random.choice(proj_group)
                if obj.texture >= 4:
                    obj.texture = -1
                obj.update_img(obj.texture+1)
                self.texture = obj.texture

        self.pos = obj.rect.center
        active = True
        angle = get_angle(obj.rect.center, A_G_V.gameSprites["player"].rect.center)
        limit1 = obj.angle-self.rotRange
        limit2 = obj.angle+self.rotRange
        if limit1 < 0:
            limit1 += 360
            limit1, limit2 = limit2, limit1
            if angle<limit1 or angle>limit2:
                self.angle = angle
            else:
                active = False
        elif angle<limit1 or angle>limit2:
            active = False
        else:
            self.angle = angle

        self.shootPos = obj.rect.move(get_vect(self.angle, 75+projectile_models[self.proj]["r"]/2)).center
        self.focusPos = A_G_V.gameSprites["player"].rect.center
        if not self.alwaysShoot and self.on:
            inf = projectile_models[self.proj]["r"]-2
            if projectile_models[self.proj]["s"] >= 25:
                inf += 4
            solid_rects = [obj.hitbox.inflate(inf+2, inf+2) for obj in A_G_V.get_solids() if obj.shape == 0]
            circles = [(obj.rect.centerx, obj.rect.centery, obj.hitbox.w/2+inf/2+4) for obj in A_G_V.get_solids() if obj.shape == 1]
            littlevect = get_vect(get_angle(A_G_V.gameSprites["player"].rect.center, self.shootPos), 11)
            endpoint = A_G_V.gameSprites["player"].rect.move(littlevect).center
            if raycast(solid_rects, circles, obj.rect.center, endpoint) is not None:
                active = False

        self.activated = active

        self.image = pygame.transform.rotate(res.images["cannon"][self.texture], self.angle)
        self.rect = self.image.get_rect(center=self.pos)

        if active and A_G_V.end is None and A_G_V.unlock and self.on and not A_G_V.gameSprites["player"].noColl and not self.onlySignal:
            self.shoot(A_G_V)

        if self.cooldown > 0:
            if A_G_V.end is None and A_G_V.unlock and self.on:
                self.cooldown -= 1
        if self.inter-2 > self.cooldown >= 25:
            self.activated = False
        if self.sniperMode and self.cooldown == 25 and A_G_V.unlock:
            res.soundMananger.playSound("prevSignal")

        if A_G_V.end is not None:
            self.activated = False

        if self.onlySignal and self.on:
            self.shoot(A_G_V)
            self.on = False

    def draw(self, window, rect):

        if self.deco is not None:
            window.blit(self.deco, rect)

    def fdraw(self, window, rect):

        window.blit(self.image, self.rect)
        if self.sniperMode and self.activated and not (self.alwaysShoot or self.onlySignal):
            pygame.draw.line(window, (255, 0, 0), self.shootPos, self.focusPos)

    def shoot(self, A_G_V):

        if self.cooldown <= 0:
            self.cooldown = self.inter
            shootAngle = spreadAngle(self.angle, self.spread)
            proj = projectile(self.shootPos, shootAngle, projectile_models[self.proj])
            A_G_V.addProj(proj, True)
            if projectile_models[self.proj]["tr"] is not None:
                A_G_V.gameSprites["particles"].add(20, 30, self.shootPos, projectile_models[self.proj]["tr"]["c"], 255, 2, 1)
            if projectile_models[self.proj]["sound"] is not None:
                res.soundMananger.playSound(projectile_models[self.proj]["sound"])

    def signal(self, signal, obj):

        if signal == "shoot":
            self.on = True
            self.cooldown = 1

class multipleShooting(shooting):

    def shoot(self, A_G_V):

        if self.cooldown == 0:
            self.cooldown = self.inter
            for i in range(0, self.spread*7, 7):
                shootAngle = self.angle+i-7*((self.spread-1)/2)
                if self.random >= 0:
                    self.proj = random.choice(proj_group)
                    if projectile_models[self.proj]["sound"] is not None:
                        res.soundMananger.playSound(projectile_models[self.proj]["sound"])
                proj = projectile(self.shootPos, shootAngle, projectile_models[self.proj])
                A_G_V.addProj(proj, True)
            if projectile_models[self.proj]["tr"] is not None:
                A_G_V.gameSprites["particles"].add(30, 40, self.shootPos, projectile_models[self.proj]["tr"]["c"], 200, 2, 1)
            if projectile_models[self.proj]["sound"] is not None:
                res.soundMananger.playSound(projectile_models[self.proj]["sound"])

class randShoot(shooting):

    def shoot(self, A_G_V):

        if self.cooldown  == 0:
            self.cooldown = random.randint(5, self.inter*2)
            shootAngle = spreadAngle(self.angle, self.spread)
            proj = projectile(self.shootPos, shootAngle, projectile_models[self.proj])
            A_G_V.addProj(proj, True)
            if projectile_models[self.proj]["tr"] is not None:
                A_G_V.gameSprites["particles"].add(20, 30, self.shootPos, projectile_models[self.proj]["tr"]["c"], 255, 2, 1)
            if projectile_models[self.proj]["sound"] is not None:
                res.soundMananger.playSound(projectile_models[self.proj]["sound"])

class seqShoot(shooting):

    def shoot(self, A_G_V):

        cdsList = [0]
        cdNb = self.inter
        for i in range(0, random.randrange(1, 4)):
            cdNb -= 5
            cdsList.append(cdNb)
        if int(self.cooldown) in cdsList:
            if self.cooldown == 0:
                self.cooldown = self.inter
            shootAngle = spreadAngle(self.angle, self.spread)
            proj = projectile(self.shootPos, shootAngle, projectile_models[self.proj])
            A_G_V.addProj(proj, True)
            if projectile_models[self.proj]["tr"] is not None:
                A_G_V.gameSprites["particles"].add(15, 30, self.shootPos, projectile_models[self.proj]["tr"]["c"], 255, 2, 1)
            if projectile_models[self.proj]["sound"] is not None:
                res.soundMananger.playSound(projectile_models[self.proj]["sound"])

class duo_shooting(shooting):

    def __init__(self, obj, shootConfig, scoreMlt):

        self.texture = obj.texture
        self.speed = shootConfig["speed"]
        self.proj = shootConfig["p"]
        self.spread = shootConfig["s"]
        self.inter = int(shootConfig["cd"]*(1/((2+scoreMlt)/3)))
        self.cooldown = random.randrange(0, self.inter)
        self.angle = int(obj.angle)
        self.shootPos = 0, 0
        self.image = pygame.transform.rotate(res.images["cannon_double"][self.texture], self.angle)
        self.pos = obj.rect.center
        self.rect = self.image.get_rect(center=self.pos)
        self.on = True
        self.rotRange = 180
        self.sniperMode = False
        self.deco = None

    def update(self, obj, A_G_V):

        self.pos = obj.rect.center
        self.angle += self.speed
        self.angle = limitangle(self.angle)
        self.cooldown -= 1
        if self.cooldown <= 0:
            if A_G_V.end is None and A_G_V.unlock and self.on:
                self.shootPos = obj.rect.move(get_vect(self.angle, 75+projectile_models[self.proj]["r"]/2)).center
                self.shoot(A_G_V)
                self.angle += 180
                self.angle = limitangle(self.angle)
                self.shootPos = obj.rect.move(get_vect(self.angle, 75+projectile_models[self.proj]["r"]/2)).center
                self.cooldown = 0
                self.shoot(A_G_V)
                self.angle += 180
                self.angle = limitangle(self.angle)
        self.image = pygame.transform.rotate(res.images["cannon_double"][self.texture], self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def signal(self, signal, obj):

        if signal == "shootOn":
            self.on = True
        elif signal == "shootOff":
            self.on = False
