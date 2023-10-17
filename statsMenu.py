# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import choice
from time import localtime

import game_values as GAMEVALUES
from fct import *
import interface
import res

class StatsMenu:

    def __init__(self):

        self.redirect = None

        self.part = 0

        self.returnButton = interface.button(res.language["return"], (683, 720))
        self.nextButton = interface.button(1, (683, 441))
        self.prevButton = interface.button(0, (683, 50))

        self.advScreen = pygame.Surface((1366, 768), SRCALPHA)

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 110)))
        launchTime = localtime(res.stats["firstLauch"])
        stat_FL = res.fonts["mainFont"].render("{}/{}/{} - {}:{}".format(insZero(launchTime[2]), insZero(launchTime[1]), launchTime[0], insZero(launchTime[3]), insZero(launchTime[4])), 1, (255, 255, 255))
        self.advScreen.blit(stat_FL, stat_FL.get_rect(topright=(1125, 100)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_FL"], 1, (200, 200, 200)), (242, 100))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 155)))
        stat_TT = res.fonts["mainFont"].render(convertTime(res.stats["totalTime"]), 1, (255, 255, 255))
        self.advScreen.blit(stat_TT, stat_TT.get_rect(topright=(1125, 145)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_TT"], 1, (200, 200, 200)), (242, 145))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 200)))
        stat_TS = res.fonts["mainFont"].render(str(int(res.stats["totalScore"])), 1, (255, 255, 255))
        self.advScreen.blit(stat_TS, stat_TS.get_rect(topright=(1125, 190)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_TS"], 1, (200, 200, 200)), (242, 190))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 245)))
        stat_DT = res.fonts["mainFont"].render("{}m".format((res.stats["distanceTraveled"]/3779.5275591).__round__(2)), 1, (255, 255, 255))
        self.advScreen.blit(stat_DT, stat_DT.get_rect(topright=(1125, 235)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_DT"], 1, (200, 200, 200)), (242, 235))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 290)))
        stat_PS = res.fonts["mainFont"].render(str(int(res.stats["projShooted"])), 1, (255, 255, 255))
        self.advScreen.blit(stat_PS, stat_PS.get_rect(topright=(1125, 280)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_PS"], 1, (200, 200, 200)), (242, 280))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 335)))
        stat_BD = res.fonts["mainFont"].render(str(int(res.stats["blockDestroyed"])), 1, (255, 255, 255))
        self.advScreen.blit(stat_BD, stat_BD.get_rect(topright=(1125, 325)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_BD"], 1, (200, 200, 200)), (242, 325))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 380)))
        stat_TD = res.fonts["mainFont"].render(str(int(res.stats["totalDamages"])), 1, (255, 255, 255))
        self.advScreen.blit(stat_TD, stat_TD.get_rect(topright=(1125, 370)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_TD"], 1, (200, 200, 200)), (242, 370))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 425)))
        stat_SD = res.fonts["mainFont"].render(str(int(res.stats["shieldsDestroyed"])), 1, (255, 255, 255))
        self.advScreen.blit(stat_SD, stat_SD.get_rect(topright=(1125, 415)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_SD"], 1, (200, 200, 200)), (242, 415))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 470)))
        stat_GF = res.fonts["mainFont"].render(str(int(res.stats["gamesFailed"])), 1, (255, 255, 255))
        self.advScreen.blit(stat_GF, stat_GF.get_rect(topright=(1125, 460)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_GF"], 1, (200, 200, 200)), (242, 460))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 515)))
        stat_LC = res.fonts["mainFont"].render(str(int(res.stats["levelsCompleted"])), 1, (255, 255, 255))
        self.advScreen.blit(stat_LC, stat_LC.get_rect(topright=(1125, 505)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_LC"], 1, (200, 200, 200)), (242, 505))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 560)))
        stat_D = res.fonts["mainFont"].render(str(int(res.stats["deaths"])), 1, (255, 255, 255))
        self.advScreen.blit(stat_D, stat_D.get_rect(topright=(1125, 550)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_D"], 1, (200, 200, 200)), (242, 550))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 605)))
        stat_DL = res.fonts["mainFont"].render("{}/{}".format(len(res.stats["discovered_levels"]), GAMEVALUES.totalLevels), 1, (255, 255, 255))
        self.advScreen.blit(stat_DL, stat_DL.get_rect(topright=(1125, 595)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_DL"], 1, (200, 200, 200)), (242, 595))

        self.advScreen.blit(res.images["statBar"][0], res.images["statBar"][0].get_rect(center=(683, 650)))
        stat_CL = res.fonts["mainFont"].render("{}/{}".format(len(res.stats["completed_levels"]), GAMEVALUES.totalLevels), 1, (255, 255, 255))
        self.advScreen.blit(stat_CL, stat_CL.get_rect(topright=(1125, 640)))
        self.advScreen.blit(res.fonts["mainFont"].render(res.language["stat_CL"], 1, (200, 200, 200)), (242, 640))

        self.statsScreen = pygame.Surface((1366, 768), SRCALPHA)

        self.statsScreen.blit(res.images["statBar"][1], res.images["statBar"][1].get_rect(center=(683, 155)))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["diff"], 1, (225, 225, 225)), (135, 145))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["stat_diffGL"], 1, (225, 225, 225)), (320, 145))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["stat_diffBL"], 1, (225, 225, 225)), (505, 145))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["stat_diffW"], 1, (225, 225, 225)), (690, 145))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["stat_diffBS"], 1, (225, 225, 225)), (875, 145))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["stat_diffBT"], 1, (225, 225, 225)), (1060, 145))

        self.statsScreen.blit(res.images["statBar"][1], res.images["statBar"][1].get_rect(center=(683, 200)))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["easy"], 1, (255, 255, 255)), (135, 190))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_easy"][0]), 1, (255, 255, 255)), (320, 190))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_easy"][4]), 1, (255, 255, 255)), (505, 190))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_easy"][1]), 1, (255, 255, 255)), (690, 190))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_easy"][2][0]), 1, (255, 255, 255)), (875, 190))
        if res.stats["diff_easy"][3][0] > 0:
            self.statsScreen.blit(res.fonts["smallMainFont"].render(convertTime2(res.stats["diff_easy"][3][1]), 1, (255, 255, 255)), (1060, 190))
        else:
            self.statsScreen.blit(res.fonts["smallMainFont"].render("--:--:--", 1, (255, 255, 255)), (1060, 190))

        self.statsScreen.blit(res.images["statBar"][1], res.images["statBar"][1].get_rect(center=(683, 245)))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["normal"], 1, (255, 255, 255)), (135, 235))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_normal"][0]), 1, (255, 255, 255)), (320, 235))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_normal"][4]), 1, (255, 255, 255)), (505, 235))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_normal"][1]), 1, (255, 255, 255)), (690, 235))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_normal"][2][0]), 1, (255, 255, 255)), (875, 235))
        if res.stats["diff_normal"][3][0] > 0:
            self.statsScreen.blit(res.fonts["smallMainFont"].render(convertTime2(res.stats["diff_normal"][3][1]), 1, (255, 255, 255)), (1060, 235))
        else:
            self.statsScreen.blit(res.fonts["smallMainFont"].render("--:--:--", 1, (255, 255, 255)), (1060, 235))

        self.statsScreen.blit(res.images["statBar"][1], res.images["statBar"][1].get_rect(center=(683, 290)))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["hard"], 1, (255, 255, 255)), (135, 280))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_hard"][0]), 1, (255, 255, 255)), (320, 280))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_hard"][4]), 1, (255, 255, 255)), (505, 280))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_hard"][1]), 1, (255, 255, 255)), (690, 280))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_hard"][2][0]), 1, (255, 255, 255)), (875, 280))
        if res.stats["diff_hard"][3][0] > 0:
            self.statsScreen.blit(res.fonts["smallMainFont"].render(convertTime2(res.stats["diff_hard"][3][1]), 1, (255, 255, 255)), (1060, 280))
        else:
            self.statsScreen.blit(res.fonts["smallMainFont"].render("--:--:--", 1, (255, 255, 255)), (1060, 280))

        self.statsScreen.blit(res.images["statBar"][1], res.images["statBar"][1].get_rect(center=(683, 335)))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["challenge_short"], 1, (150, 180, 255)), (135, 325))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_challenge"][0]), 1, (255, 255, 255)), (320, 325))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_challenge"][4]), 1, (255, 255, 255)), (505, 325))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_challenge"][1]), 1, (255, 255, 255)), (690, 325))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_challenge"][2][0]), 1, (255, 255, 255)), (875, 325))
        if res.stats["diff_challenge"][3][0] > 0:
            self.statsScreen.blit(res.fonts["smallMainFont"].render(convertTime2(res.stats["diff_challenge"][3][1]), 1, (255, 255, 255)), (1060, 325))
        else:
            self.statsScreen.blit(res.fonts["smallMainFont"].render("--:--:--", 1, (255, 255, 255)), (1060, 325))

        self.statsScreen.blit(res.images["statBar"][1], res.images["statBar"][1].get_rect(center=(683, 380)))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(res.language["s-challenge_short"], 1, (255, 150, 150)), (135, 370))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_s-challenge"][0]), 1, (255, 255, 255)), (320, 370))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_s-challenge"][4]), 1, (255, 255, 255)), (505, 370))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_s-challenge"][1]), 1, (255, 255, 255)), (690, 370))
        self.statsScreen.blit(res.fonts["smallMainFont"].render(str(res.stats["diff_s-challenge"][2][0]), 1, (255, 255, 255)), (875, 370))
        if res.stats["diff_s-challenge"][3][0] > 0:
            self.statsScreen.blit(res.fonts["smallMainFont"].render(convertTime2(res.stats["diff_s-challenge"][3][1]), 1, (255, 255, 255)), (1060, 370))
        else:
            self.statsScreen.blit(res.fonts["smallMainFont"].render("--:--:--", 1, (255, 255, 255)), (1060, 370))


    def update(self, animBg):

        animBg.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.redirect = "q"
            elif event.type == MOUSEMOTION:
                self.returnButton.mousePos = scalePos(event.pos)
                self.nextButton.mousePos = scalePos(event.pos)
                self.prevButton.mousePos = scalePos(event.pos)
            elif event.type == MOUSEBUTTONDOWN:
                if self.returnButton.click():
                    self.redirect = "main"
                elif self.part == 0 and self.nextButton.click():
                    self.part = 1
                elif self.part == 1 and self.prevButton.click():
                    self.part = 0

        self.returnButton.update()
        if self.part == 0:
            self.nextButton.update()
        else:
            self.prevButton.update()

    def show(self, window, animBg):

        animBg.draw(window)
        if self.part == 0:
            window.blit(self.statsScreen, (0, 0))
            self.nextButton.draw(window)
        else:
            window.blit(self.advScreen, (0, 0))
            self.prevButton.draw(window)
        self.returnButton.draw(window)
