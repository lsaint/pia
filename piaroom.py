# -*- coding: utf-8 -*-

from show import Show
import const


class PiaRoom(object):

    def __init__(self, chl):
        self.chl = chl
        self.socket2player = {}
        self.show = None


    def getPlayer(self, s):
        return self.socket2player.get(s)


    def getShow(self):
        return self.show


    def createShow(self, director, scid, name, roles):
        show = Show(director, scid, name, roles)
        self.show = show
        return show


    def comein(self, player):
        if len(self.socket2player) >= const.MAX_ROOM_PLAYER:
            return False
        self.socket2player[player.socket] = player
        print "comein", self.socket2player
        return True


    def leave(self, s):
        player = self.socket2player.get(s)
        if player is not None:
            if self.show:
                self.show.leave(player)

            del self.socket2player[s]


    def cancelShow(self):
        print "cancelShow"
        self.show = None
        bc = {"Op":"CancelShow"}
        self.broadcast(bc)


    def broadcast(self, msg):
        print "room.broadcast", self.socket2player
        for s, player in self.socket2player.items():
            player.send(msg)


    def update(self):
        if self.getShow():
            self.show.update()

