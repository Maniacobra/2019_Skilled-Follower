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

class destroySignal(instance):

    def __init__(self, obj, param, scoreMlt):

        self.f = False
        self.target = param["tar"]
        self.signal_message = param["signal"]

    def endAction(self, obj, A_G_V): A_G_V.sendSignal(self.target, self.signal_message)

    def update(self, obj, A_G_V):

        A_G_V.gameSprites["particles"].add(1, 7, obj.rect.center, (230, 255, 230), 255, obj.rect.width/2, 0.5)

class hitSignal(instance):

    def __init__(self, obj, param, scoreMlt):

        self.f = False
        self.target = param["tar"]
        self.signal_message = param["signal"]

    def hitAction(self, obj, A_G_V): A_G_V.sendSignal(self.target, self.signal_message)

class zoneSignal(instance):

    def __init__(self, obj, param, scoreMlt):

        self.target = param["tar"]
        self.onSignal = param["signalOn"]
        self.offSignal = param["signalOff"]
        self.mode = param["m"]
        self.playerOn = False
        self.toggle = False
        self.nbPress = 0

    def update(self, obj, A_G_V):

        if not (self.mode == 2 and self.nbPress > 0):
            if obj.collide(A_G_V.gameSprites["player"].rect):
                if not self.playerOn:
                    if self.mode == 1 and self.toggle:
                        self.toggle = False
                        A_G_V.sendSignal(self.target, self.offSignal)
                    else:
                        self.toggle = True
                        A_G_V.sendSignal(self.target, self.onSignal)
                        self.nbPress += 1
                    self.playerOn = True
            elif self.playerOn:
                if self.mode == 0:
                    A_G_V.sendSignal(self.target, self.offSignal)
                self.playerOn = False

class clockSignal(instance):

    def __init__(self, obj, param, scoreMlt):

        self.target = param["tar"]
        self.onSignal = param["signalOn"]
        self.offSignal = param["signalOff"]
        self.phase1 = param["p1"]
        self.phase2 = param["p2"]
        self.count = self.phase1
        self.phase = 0

    def update(self, obj, A_G_V):

        if self.count == 0:
            if self.phase == 0:
                A_G_V.sendSignal(self.target, self.onSignal)
                self.count = self.phase2
                self.phase = 1
            else:
                A_G_V.sendSignal(self.target, self.offSignal)
                self.count = self.phase1
                self.phase = 0
        self.count -= 1

class signalCondition(instance):

    def __init__(self, obj, param, scoreMlt):

        self.target = param["tar"]
        self.signal_message = param["signal"]
        self.count = param["nb"]
        self.showCount = param["show"]
        self.messagesList = []
        self.end = False

    def update(self, obj, A_G_V):

        if not self.end and len(self.messagesList) >= self.count:
            self.end = True
            A_G_V.sendSignal(self.target, self.signal_message)

    def signal(self, signal, obj):

        if signal not in self.messagesList and signal != "-":
            self.messagesList.append(signal)

    def draw(self, window, rect):

        if self.showCount:
            text = res.fonts["digital"].render("{}/{}".format(len(self.messagesList), self.count), 1, (120, random.randint(120, 255), 120))
            window.blit(text, text.get_rect(center=(rect.centerx, rect.centery-1)))

class delaySignal(instance):

    def __init__(self, obj, param, scoreMlt):

        self.delay = int(param["t"]*60)
        self.signal_message = param["signal"]
        self.target = param["tar"]
        self.cooldown = 0

    def update(self, obj, A_G_V):

        if self.cooldown > 0:
            self.cooldown -= 1
            if self.cooldown == 0:
                A_G_V.sendSignal(self.target, self.signal_message)

    def signal(self, signal, obj):

        if signal == "start":
            self.cooldown = self.delay
