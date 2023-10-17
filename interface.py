# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

import res
from fct import *

class button(pygame.sprite.Sprite):

    def __init__(self, text, pos, small=False, sounds=0):

        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.mouseOn = False
        self.colored = 0
        self.mousePos = scalePos(pygame.mouse.get_pos())
        self.sounds = sounds
        self.pos = pos
        self.small = small
        self.imgUpdate()
        self.clicBox = self.rect

    def imgUpdate(self):

        if self.text == 0:
            text = pygame.Surface((30, 30), SRCALPHA)
            pygame.draw.polygon(text, (255, 255, 255-self.colored), [(15, 0), (0, 30), (30, 30)])
        elif self.text == 1:
            text = pygame.Surface((30, 30), SRCALPHA)
            pygame.draw.polygon(text, (255, 255, 255-self.colored), [(15, 30), (0, 0), (30, 0)])
        else:
            if self.small:
                text = res.fonts["smallButtons"].render(self.text, 1, (255, 255, 255-self.colored))
            else:
                text = res.fonts["buttons"].render(self.text, 1, (255, 255, 255-self.colored))
        self.rect = text.get_rect().inflate(10, 10)
        self.rect.center = self.pos
        if self.mouseOn:
            self.rect = self.rect.move(-10, 0)
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        self.image.fill((40, 40, 40))
        pygame.draw.rect(self.image, (200, 200, 200), (0, 0, self.rect.w, self.rect.h), 2)
        self.image.blit(text, (5, 6))

    def update(self):

        if self.clicBox.collidepoint(self.mousePos):
            if self.mouseOn == False:
                if self.sounds == 0:
                    res.soundMananger.playSound("bip")
                self.rect = self.rect.move(-10, 0)
                self.imgUpdate()
            self.imgUpdate()
            self.image = pygame.transform.scale(self.image, (self.image.get_width()+20, self.image.get_height()+10))
            self.mouseOn = True
            self.colored = 200
        elif self.mouseOn:
            self.rect = self.rect.move(10, 0)
            self.imgUpdate()
            self.mouseOn = False
        elif self.colored >= 5:
            self.colored -= 5
            self.imgUpdate()

    def draw(self, window):

        window.blit(self.image, self.rect)

    def changeText(self, text, small=None):

        if small is not None:
            self.small = small
        if self.mouseOn:
            rgb = (255, 255, 70)
        else:
            rgb = (255, 255, 255)
        self.text = text
        self.imgUpdate()

    def reinit(self):

        self.mousePos = scalePos(pygame.mouse.get_pos())
        self.colored = 0
        self.imgUpdate()
        self.mouseOn = False
        self.rect = self.clicBox

    def click(self):

        if self.mouseOn:
            if self.sounds == 0:
                res.soundMananger.playSound("click")
            return True

class slider:

    def __init__(self, y, ratio, limit=(503, 863)):

        self.image = pygame.Surface((15, 30))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect(center=(limit[0]+(limit[1]-limit[0])*ratio, y))
        self.catched = False
        self.limit = limit

    def slide(self, mouseX):

        if mouseX < self.limit[0]:
            self.rect.centerx = self.limit[0]
        elif mouseX > self.limit[1]:
            self.rect.centerx = self.limit[1]
        else:
            self.rect.centerx = mouseX
        return (self.rect.centerx-self.limit[0])/(self.limit[1]-self.limit[0])

    def catch(self, mousePos):

        if self.rect.collidepoint(mousePos):
            self.catched = True
            self.image.fill((255, 255, 255))

    def uncatch(self):

        if self.catched:
            self.catched = False
            self.image.fill((200, 200, 200))
            return True

    def draw(self, window):

        pygame.draw.line(window, (150, 150, 150), (self.limit[0], self.rect.centery), (self.limit[1], self.rect.centery), 5)
        window.blit(self.image, self.rect)
