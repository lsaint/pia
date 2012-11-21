# -*- coding: utf-8 -*-

import gevent, json

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


    def broadcast(self, s, **k):
        print "broadcast"
        room = self.getRoomBySocket(s)
        if room:
            room.broadcast(k["Msg"])


    def login(self, s, **k):
        print "login"
        chl = k["Cid"]
        room = self.getRoomByChl(k["Cid"])
        if not room:
            room = PiaRoom(chl)
        self.registerRoom(chl, s, room)
        player = Player(k["Uid"], k["Name"], room, s)
        ret = room.comein(player)
        rep = {"Ret":const.RET_FL, "Op":"login"}
        if ret:
            rep["Ret"] = const.RET_OK
        player.send(rep)


    def logout(self, s, **k):
        print "logout", s
        room = self.getRoomBySocket(s)
        if room:
            print room
            room.leave(s)
        if self.getRoomBySocket(s) is not None:
            del self.socket2room[s]


    def createShow(self, s, **k):
        room = self.getRoomBySocket(s)
        rep = {"Ret":const.RET_FL, "Op":"create_show"}
        if not room or room.getShow() is not None or room.getPlayer(s) is None:
            return self.reply(s, rep)
        rep["Ret"] = const.RET_OK
        self.reply(s, rep)

        show = room.createShow(room.getPlayer(s), k["Scid"], k["Name"], k["Roles"])
        broadcast_crate_show_msg = {"Scid":show.scid, "Name":show.name,\
                "Roles":show.roles, "Op":"create_show_bc"}
        room.broadcast(broadcast_crate_show_msg)


    def disconnect(self, s):
        self.logout(s)


    def reply(self, s, msg):
        s.sendall(json.dumps(msg) + const.DELIMITER)

