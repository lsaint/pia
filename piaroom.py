# -*- coding: utf-8 -*-


class PiaRoom(object):

    def __init__(self, chl):
        self.chl = chl
        self.socket2player = {}


    def comein(self, player):
        self.socket2player[player.socket] = player


    def leave(self, s):
        if self.socket2player.get(s) is not None:
            del(self.socket2player, s)

