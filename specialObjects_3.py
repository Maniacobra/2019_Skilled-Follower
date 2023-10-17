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

class anim(instance):

    def __init__(self, obj, frames, scoreMlt):

        self.img = 0
        self.frames = 60/frames["f"]
        self.count = self.frames
        self.on = True

    def update(self, obj, A_G_V):

        if self.on:
            if self.count <= 0:
                self.count = self.frames
                self.img += 1
                if self.img > len(res.images[obj.name])-1:
                    self.img = 0
                obj.image = res.images[obj.name][self.img]
            else:
                self.count -= 1

    def signal(self, signal, obj):

        if signal == "stopAnim":
            self.on = False
        elif signal == "startAnim":
            self.on = True

class randRot(instance):

    def __init__(self, obj, range, scoreMlt):

        self.angle = random.randrange(0, 360, range["range"])
        self.f = False

    def firstAction(self, obj, A_G_V):

        obj.image = rot_center(obj.image, self.angle)

class rotate(instance):

    def __init__(self, obj, speed, scoreMlt):

        self.speed = speed["s"]
        if speed["r"]:
            if random.getrandbits(1) == 0:
                self.speed *= -1
        self.image = obj.image
        self.rot = 0

    def update(self, obj, A_G_V):

        self.rot += self.speed
        obj.image = rot_center(self.image, self.rot)

class colorShape(instance):

    def __init__(self, obj, shape, scoreMlt):

        self.f = False
        self.color = shape["r"], shape["v"], shape["b"]

    def draw(self, window, rect):

        pygame.draw.rect(window, self.color, rect)

class contact_button(instance):

    def __init__(self, obj, mode, scoreMlt):

        self.mode = mode["m"]
        self.playerOn = False
        self.toggle = False

    def update(self, obj, A_G_V):

        if obj.collide(A_G_V.gameSprites["player"].rect):
            if not self.playerOn:
                if self.mode == 1:
                    if self.toggle:
                        self.toggle = False
                        obj.update_img(0)
                    else:
                        self.toggle = True
                        obj.update_img(1)
                    res.soundMananger.playSound("button")
                elif obj.texture == 0:
                    obj.update_img(1)
                    res.soundMananger.playSound("button")
                self.playerOn = True
        elif self.playerOn:
            if self.mode == 0:
                obj.update_img(0)
                res.soundMananger.playSound("button")
            self.playerOn = False

class door(instance):

    def __init__(self, obj, param, scoreMlt):

        if obj.texture == 1:
            obj.solid = False
        self.action = 0
        self.movement_flow = -1

    def update(self, obj, A_G_V):

        if self.action == 1:
            if self.movement_flow == 20:
                self.action = 0
                obj.solid = False
                obj.update_img(1)
                self.movement_flow = -1
            else:
                obj.image = pygame.transform.rotate(res.images["a-door"][self.anim_state()], obj.ortho_angle)
            self.movement_flow += 1
        elif self.action == 2:
            if self.movement_flow < 10:
                if obj.collide(A_G_V.gameSprites["player"].rect):
                    A_G_V.loose()
            if self.movement_flow == 0:
                self.action = 0
                obj.solid = True
                obj.update_img(0)
            else:
                obj.image = pygame.transform.rotate(res.images["a-door"][self.anim_state()], obj.ortho_angle)
            self.movement_flow -= 1

    def signal(self, signal, obj):

        if signal == "doorOpen" and obj.texture == 0:
            res.soundMananger.playSound("door")
            self.action = 1
        elif signal == "doorClose" and obj.texture == 1:
            res.soundMananger.playSound("door")
            self.action = 2
            self.movement_flow = 19

    def anim_state(self):

        if self.movement_flow > 16:
            return 4
        elif self.movement_flow > 12:
            return 3
        elif self.movement_flow > 8:
            return 2
        elif self.movement_flow > 4:
            return 1
        else:
            return 0
