# -*- coding: utf-8 -*-

import gevent

from piaroom import PiaRoom
from player  import Player
import const


class PiaMgr(object):

    socket2room = {}
    chl2room = {}

    def __init__(self):
        pass


    def getRoomBySocket(self, s):
        return self.socket2room.get(s)


    def getRoomByChl(self, chl):
        return self.chl2room.get(chl)


    def registerRoom(self, chl, s, room):
        self.socket2room[s] = room
        self.chl2room[chl] = room


    def checkPings(self):
        while True:
            gevent.sleep(const.PING_INTERVAL)


    def broadcast(self, s, **kwargs):
        print "broadcast"
        room = self.getRoomBySocket(s)
        if room:
            room.broadcast(kwargs["Msg"])


    def login(self, s, **kwargs):
        print "login"
        chl = kwargs["Cid"]
        room = self.getRoomByChl(kwargs["Cid"])
        if not room:
            room = PiaRoom(chl)
        self.registerRoom(room.chl, s, room)
        player = Player(kwargs["Uid"], kwargs["Name"], room, s)
        room.comein(player)
        player.send({"Ret":const.RET_OK, "Op":"login"})


    def logout(self, s, **kwargs):
        print "logout", s
        room = self.getRoomBySocket(s)
        if room:
            print room
            room.leave(s)
        if self.getRoomBySocket(s) is not None:
            del self.socket2room[s]


    def disconnect(self, s):
        self.logout(s)


