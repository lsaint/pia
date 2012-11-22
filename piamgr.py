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


    def onBroadcast(self, room, player, **k):
        print "broadcast"
        room.broadcast(k["Msg"])


    def onLogin(self, s, **k):
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


    def onLogout(self, room, player, **k):
        print "logout"
        room.leave(player.socket)
        del self.socket2room[player.socket]


    def onCreateShow(self, room, player, **k):
        print "createShow"
        rep = {"Ret":const.RET_FL, "Op":"create_show"}
        if room.getShow() is not None :
            return player.send(rep)
        rep["Ret"] = const.RET_OK
        player.send(rep)

        show = room.createShow(player, k["Scid"], k["Name"], k["Roles"])
        broadcast_crate_show_msg = {"Scid":show.scid, "Name":show.name,\
                "Roles":show.roles, "Op":"create_show_bc"}
        room.broadcast(broadcast_crate_show_msg)


    def onApplyRole(self, room, player, **k):
        rep = {"Ret":const.RET_FL, "Op":k["Op"]}
        if  not room.getShow():
            return player.send(rep)


    def disconnect(self, s):
        self.commonCheck(s, **{"Op":"Logout"})


    def reply(self, s, msg):
        s.sendall(json.dumps(msg) + const.DELIMITER)


    def commonCheck(self, s, **k):
        room = self.getRoomBySocket(s)
        if room:
            player = room.getPlayer(s)
            if player:
                method = getattr(self, "on" + k["Op"])
                method(room, player, **k)
            else:
                print "player not in room"
        else:
            print "commonCheck fail"
            self.reply(s, {"Ret":const.RET_FL, "Op":k["Op"]})

