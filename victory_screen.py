# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

import game_values as GAMEVALUES
from fct import *
import interface
from visuals import *
import res

class VictoryScreen:

    def __init__(self, score, levelTimes, diff):

        self.redirect = None

        self.levelTimes = levelTimes
        self.chrono = levelTimes[-1].__round__(2)
        self.score = int(score)
        self.diff = diff
        self.count = 300
        self.leaveCD = -1
        self.fadeEffect = pygame.sprite.GroupSingle()
        self.textColor1 = [255, 255, 255]
        self.textColor2 = [255, 255, 255]
        self.bestTime = False
        self.bestScore = False

        if self.chrono == res.stats[res.get_diff(diff)][3][1]:
            print("[INFO] MEILLEUR TEMPS")
            self.textColor1 = [254, 100, 100]
            self.bestTime = True
        if self.score == int(res.stats[res.get_diff(diff)][2][0]):
            print("[INFO] MEILLEUR SCORE")
            self.textColor2 = [100, 253, 100]
            self.bestScore = True

        self.title = res.fonts["title"].render(res.language["victory"], 1, (255, 255, 255))
        self.titleRect = self.title.get_rect(center=(683, -100))

        self.timeBar = pygame.Surface((1000, 50))
        self.timeBar.fill((180, 180, 210))
        pygame.draw.rect(self.timeBar, (255, 255, 255), self.timeBar.get_rect(), 5)
        pygame.draw.rect(self.timeBar, (0, 0, 0), self.timeBar.get_rect(), 1)
        px_ratio = 1000/self.chrono
        self.line_frames = 150
        self.nb_line = 0
        self.lineList = []
        for time in self.levelTimes:
            self.lineList.append(time*px_ratio)
        self.timeBar.set_alpha(0)
        self.showTime = res.fonts["mainFont"].render("{} : {}".format(res.language["gameTime"], convertTime2(self.chrono)), 1, (255, 255, 255))
        self.totalScore = res.fonts["mainFont"].render("{} : {}".format(res.language["gameScore"], int(self.score)), 1, (255, 255, 255))
        self.difficulty = res.fonts["mainFont"].render("{} : {}".format(res.language["diff"], res.language[res.get_diff(diff)[5:]]), 1, (255, 255, 255))
        self.totalWin = res.fonts["mainFont"].render("{} : {}".format(res.language["stat_diffW"], res.stats[res.get_diff(diff)][1]), 1, (255, 255, 255))

        self.levelSelected = len(self.lineList)-1
        self.clicked = False
        self.selectRect = None

        self.beamDeco = []
        self.beamCount = 180

    def update(self):

        if self.count > 0:
            self.count -= 1
            if self.count == 240:
                res.soundMananger.playMusic(2)
        self.beamCount -= 1
        if self.beamCount == 0:
            self.beamDeco.append(falling_beam())
            self.beamCount = 5
        for beam in self.beamDeco:
            beam.update()
            if beam.speed == 0:
                self.beamDeco.remove(beam)

        if self.textColor1[1] < 254 and self.textColor1[2] == 100:
            self.textColor1[0] -= 2
            self.textColor1[1] += 2
        elif self.textColor1[2] < 254 and self.textColor1[0] == 100:
            self.textColor1[1] -= 2
            self.textColor1[2] += 2
        elif self.textColor1[0] < 254 and self.textColor1[1] == 100:
            self.textColor1[2] -= 2
            self.textColor1[0] += 2

        if self.textColor2[1] > 100 and self.textColor2[2] == 100:
            self.textColor2[0] += 3
            self.textColor2[1] -= 3
        elif self.textColor2[2] > 100 and self.textColor2[0] == 100:
            self.textColor2[1] += 3
            self.textColor2[2] -= 3
        elif self.textColor2[0] > 100 and self.textColor2[1] == 100:
            self.textColor2[2] += 3
            self.textColor2[0] -= 3

        for event in pygame.event.get():
            if event.type == QUIT:
                self.redirect = "q"
            elif event.type == KEYDOWN and self.count < 50 and self.leaveCD < 0:
                self.fadeEffect.add(fade((0, 0, 0), 255, 60))
                self.leaveCD = 60
            elif event.type == MOUSEMOTION and self.count < 20:
                self.levelSelected = len(self.lineList)-1
                if pygame.Rect(183, 374, 1000, 50).collidepoint(event.pos):
                    i = 0
                    leftborder = 183
                    r_leftborder = self.lineList[-1]
                    rightborder = 1183
                    r_rightborder = rightborder
                    for line in self.lineList:
                        if event.pos[0] < 183+line:
                            if i == 0:
                                r_leftborder = leftborder
                            else:
                                r_leftborder = 183+self.lineList[i-1]
                            if i < len(self.lineList)-1:
                                r_rightborder = 183+line
                            self.levelSelected = i
                            break
                        i += 1
                    self.selectRect = pygame.Rect(r_leftborder+5, 379, r_rightborder-r_leftborder-10, 40)
                else:
                    self.selectRect = None
            elif event.type == MOUSEBUTTONDOWN and self.count < 20:
                if self.levelSelected < len(self.lineList)-1:
                    self.clicked = True
                    self.showTime = res.fonts["mainFont"].render("{} {} : {}".format(res.language["levelTime"], self.levelSelected+1, convertTime2(self.levelTimes[self.levelSelected])), 1, (255, 255, 255))
                else:
                    self.clicked = False
                    if not self.bestTime:
                        self.showTime = res.fonts["mainFont"].render("{} : {}".format(res.language["gameTime"], convertTime2(self.chrono)), 1, (255, 255, 255))
        if self.bestTime and not self.clicked:
            self.showTime = res.fonts["mainFont"].render("{} : {} ({})".format(res.language["gameTime"], convertTime2(self.chrono), res.language["best"]), 1, self.textColor1)
        if self.bestScore:
            self.totalScore = res.fonts["mainFont"].render("{} : {} ({})".format(res.language["gameScore"], int(self.score), res.language["best"]), 1, self.textColor2)

        if self.count > 150:
            self.titleRect = self.titleRect.move(0, (self.count-150)/150*6.12)
        if 100 < self.count < 200:
            self.timeBar.set_alpha((200-(self.count-100)*2)/100*255)
        if self.count == self.line_frames and self.nb_line < len(self.lineList):
            self.line_frames -= 8
            if len(self.lineList)-1 > self.nb_line:
                pygame.draw.line(self.timeBar, (255, 255, 255), (self.lineList[self.nb_line], 0), (self.lineList[self.nb_line], 50), 5)
            self.nb_line += 1
        elif self.count == self.line_frames+3 and len(self.lineList) > self.nb_line > 0:
            pygame.draw.line(self.timeBar, (0, 0, 0), (self.lineList[self.nb_line-1], 0), (self.lineList[self.nb_line-1], 50), 5)
            pygame.draw.line(self.timeBar, (255, 255, 255), (self.lineList[self.nb_line-1], 1), (self.lineList[self.nb_line-1], 48), 3)
            res.soundMananger.playSound("ding")

        self.fadeEffect.update()
        if self.leaveCD > 0:
            self.leaveCD -= 1
            if self.leaveCD == 0:
                self.redirect = "endGame"

    def show(self, window):

        limit = 1
        if self.count > limit:
            color = int(self.count/300*255)
        else:
            color = limit/300*255
        window.fill((color, color, color))
        for beam in self.beamDeco:
            beam.draw(window)
        window.blit(self.title, self.titleRect)
        window.blit(self.timeBar, (183, 374))
        if self.nb_line == len(self.lineList):
            window.blit(self.showTime, self.showTime.get_rect(center=(683, 465)))
            window.blit(self.totalScore, self.totalScore.get_rect(center=(683, 495)))
            window.blit(self.difficulty, self.difficulty.get_rect(center=(683, 550)))
            window.blit(self.totalWin, self.totalWin.get_rect(center=(683, 580)))
            if self.selectRect is not None:
                window.fill((220, 220, 255), self.selectRect)
        if self.levelSelected < len(self.levelTimes) and self.selectRect is not None:
            if self.levelSelected > 0:
                window.blit(res.fonts["impact"].render(convertTime2(self.levelTimes[self.levelSelected]-self.levelTimes[self.levelSelected-1]), 1, (255, 255, 255)), (self.selectRect.centerx-35, 348))
            else:
                window.blit(res.fonts["impact"].render(convertTime2(self.levelTimes[self.levelSelected]), 1, (255, 255, 255)), (self.selectRect.centerx-35, 348))
        self.fadeEffect.draw(window)
