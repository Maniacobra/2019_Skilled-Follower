# -*- coding: utf-8 -*-

import pygame
import math
from random import randrange

import game_values as GAMEVALUES
from fct import *
from visuals import *
import res
from proj_models import projectile_models

class instance:

    def __init__(self, proj, args):

        self.f_action = False

    def update(self, proj, A_G_V):

        if not self.f_action:
            self.f_action = True
            self.firstAction(proj, A_G_V)

    def firstAction(self, proj, A_G_V):

        pass

    def endAction(self, proj, A_G_V):

        pass

class electron(instance):

    def __init__(self, proj, unstability):

        self.f_action = False
        self.var = unstability["u"]

    def update(self, proj, A_G_V):

        proj.pos[0] = proj.pos[0] + randint(-self.var, self.var)
        proj.pos[1] = proj.pos[1] + randint(-self.var, self.var)

class follow(instance):

    def __init__(self, proj, force):

        self.f_action = False
        self.force = force["f"]

    def update(self, proj, A_G_V):

        if A_G_V.end is None:
            speed = proj.speed/(math.sqrt(self.force))*2
            angle = get_angle(proj.rect.center, A_G_V.gameSprites["player"].rect.center)
            motion1 = get_vect(angle, speed)
            motion2 = get_vect(get_angle((0, 0), proj.motion), speed)
            mx = motion2[0]+motion1[0]/self.force
            my = motion2[1]+motion1[1]/self.force
            proj.motion = mx, my
            proj.image = pygame.transform.rotate(res.images["projectiles"][proj.id], get_angle((0, 0), proj.motion))

        sameProjs = [pr for pr in A_G_V.gameSprites["hazardProjectiles"] if pr.id == proj.id and pr != proj]
        for pr in comparePGE(proj.pGEs, sameProjs):
            if collideCircle(proj.rect, pr.rect):
                pr.delete = True

class doubleVerif(instance):

    def update(self, proj, A_G_V):

        rect = proj.rect.move(proj.motion[0]/-2, proj.motion[1]/-2)
        if proj.trail is not None:
            A_G_V.gameSprites["particles"].add(proj.trail["n"], proj.trail["f"], rect.center, proj.trail["c"], proj.trail["o"], proj.trail["z"], proj.trail["d"])
        if proj.damages == -1 and A_G_V.end is None:
            hitbox = proj.hitbox.move(proj.motion[0]/-2, proj.motion[1]/-2)
            self.pGE, self.pGEs = pG_rectLeaving(rect, A_G_V.partialGrid[1][proj.pGE], proj.pGE)
            if len(comparePGE(A_G_V.gameSprites["player"].pGEs, (proj,))) > 0:
                if collideCircle(A_G_V.gameSprites["player"].rect, hitbox):
                    proj.kill()
                    A_G_V.loose()

class gravity(instance):

    def __init__(self, proj, force):

        self.f_action = False
        self.force = force["f"]

    def update(self, proj, A_G_V):

        proj.motion[1] += self.force
        angle = get_angle(proj.pos, (proj.pos[0]+proj.motion[0], proj.pos[1]+proj.motion[1]))
        proj.image = pygame.transform.rotate(res.images["projectiles"][proj.id], angle)

class ghost(instance):

    def __init__(self, proj, param):

        self.f_action = False
        proj.magic = True

class explode(instance):

    def __init__(self, proj, param):

        self.f_action = False

        self.nbFrag = param["nbFrag"]
        self.radius = param["r"]
        self.damages = param["dmg"]
        self.color = param["c"]
        self.projName = param["p"]

    def endAction(self, proj, A_G_V):

        res.soundMananger.playSound("bombExp1")
        angle = randrange(0, int(360/self.nbFrag))
        A_G_V.gameSprites["visuals"].add(growingCircle(proj.pos, 75, 6, self.color))
        for i in range(0, self.nbFrag):
            A_G_V.addProj_args(proj.pos, angle, projectile_models[self.projName])
            angle += 360/self.nbFrag
        for obj in A_G_V.get_solids():
            if obj.collide(proj.rect.inflate(self.radius, self.radius)):
                obj.hit(self.damages, get_vect(get_angle(proj.rect.center, obj.rect.center), 10), False)

class disappear(instance):

    def __init__(self, proj, param):

        self.f_action = False
        self.lifetime = param["life"]
        self.lifetime += (randrange(0, 30)-15)

    def update(self, proj, A_G_V):

        self.lifetime -= 1
        if self.lifetime == 0:
            proj.delete = True

class bounce(instance):

    def __init__(self, proj, param):

        self.f_action = False
        self.bounce_nb = param["b"]
        self.delete = False
        proj.magic = True
        self.reboundCd = 5

    def update(self, proj, A_G_V):

        if self.reboundCd == 0:
            if not 30 <= proj.pos[0] <= 1346:
                proj.motion[0] *= -1
                self.bounce(proj)
            elif not 30 <= proj.pos[1] <= 738:
                proj.motion[1] *= -1
                self.bounce(proj)
            else:
                testSprites = comparePGE(proj.pGEs, A_G_V.get_solids(True))
                inflated = proj.hitbox.inflate(10, 10)
                inflated.center = proj.pos
                for obstacle in testSprites:
                    if obstacle.collide(inflated):
                        if obstacle.shape == 0:
                            if math.fabs(obstacle.hitbox.centerx-(proj.pos[0]-proj.motion[0]*10)) < math.fabs(obstacle.hitbox.centery-(proj.pos[1]-proj.motion[1]*10)):
                                proj.motion[1] *= -1
                            else:
                                proj.motion[0] *= -1
                        else:
                            proj.motion = get_vect(get_angle(obstacle.hitbox.center, proj.pos), proj.speed)
                        self.bounce(proj)
                        break
        else:
            self.reboundCd -= 1

    def bounce(self, proj):

        self.reboundCd = 5
        if self.bounce_nb > 0:
            self.bounce_nb -= 1
            if self.bounce_nb == 0:
                proj.id = 13
            proj.image = pygame.transform.rotate(res.images["projectiles"][proj.id], get_angle_fromVect(proj.motion))
            res.soundMananger.playSound("bounce")
            proj.pos[0] += proj.motion[0]
            proj.pos[1] += proj.motion[1]
        else:
            res.soundMananger.playSound("projDes")
            proj.delete = True

class shooting(instance):

    def __init__(self, proj, param):

        self.f_action = False

        self.projName = param["p"]
        self.inter = param["cd"]
        self.cd = 0

    def update(self, proj, A_G_V):

        if self.cd > 0:
            self.cd -= 1
        else:
            if A_G_V.end is None and A_G_V.gameSprites["player"].outStart:
                self.cd = self.inter*((A_G_V.scoreMultiplier+1)/2)
                pos = proj.pos[0]+proj.motion[0]*2, proj.pos[1]+proj.motion[1]*2

                angle = get_angle(proj.pos, A_G_V.gameSprites["player"].rect.center)
                A_G_V.addProj_args(pos, angle, projectile_models[self.projName])
                A_G_V.addProj_args(pos, angle-2, projectile_models[self.projName])
                A_G_V.addProj_args(pos, angle+2, projectile_models[self.projName])

                res.soundMananger.playSound(projectile_models[self.projName]["sound"])
