# -*- coding: utf-8 -*-

class instance:

    def __init__(self, obj, param, scoreMlt):

        self.f = False

    def update(self, obj, A_G_V):

        if not self.f:
            self.f = True
            self.firstAction(obj, A_G_V)

    def firstAction(self, obj, A_G_V):

        pass

    def endAction(self, obj, A_G_V):

        pass

    def hitAction(self, obj, A_G_V):

        pass

    def sdraw(self, window, rect):

        pass

    def draw(self, window, rect):

        pass

    def fdraw(self, window, rect):

        pass

    def signal(self, signal, obj):

        pass
