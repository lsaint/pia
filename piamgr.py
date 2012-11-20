# -*- coding: utf-8 -*-

import gevent

from piaroom import PiaRoom
from player  import Player


class PiaMgr(object):

    chl2room = {}
    pings = {}

    def __init__(self):
        pass


    def getRoom(self, chl):
        return self.chl2room.get(chl)


    def registerRoom(self, room):
        self.chl2room[room.chl] = room


    def loop(self):
        while True:
            print "loop"
            gevent.sleep(1)


    def broadcast(self, s, **kwargs):
        print "broadcast", kwargs


    def login(self, s, **kwargs):
        print "login", kwargs
        chl = kwargs["Cid"]
        room = self.getRoom(chl)
        if not room:
            room = PiaRoom(chl)
            self.registerRoom(room)
        player = Player(uid, kwargs["Uid"], kwargs["Name"], room, s)
        room.comein(player)


    def logout(self, s, **kwargs):
        pass


