# -*- coding: utf-8 -*-

import time

import const


class Show(object):

    def __init__(self, director, scid, name, roles):
        self.director = director
        self.room = director.room
        self.scid = scid
        self.name = name
        self.roles = roles
        self.actors = {}
        #self.applying = {}
        self.status = const.SHOW_STATUS_APPLY
        self.create_time = int(time.time())


    def getShowInfo(self):
        actors = {}
        for roid, player in self.actors.items():
            actors[roid] = player.uid

        t = int(time.time()) - self.create_time
        if t > const.APPLY_TIME:
            t -= const.APPLY_TIME
        if t > const.PREPARE_TIME:
            t -= const.PREPARE_TIME

        return {"Director":self.director.uid,\
                "Scid":self.scid,
                "Name":self.name,
                "Roles":self.roles,
                "Actor":actors,
                "Status":self.status,
                "Time":t}


    def applyRole(self, player, roid):
        print "applyRole"
        #self.applying[player] = roid
        if self.actors.get(roid) is not None:
            return False
        self.director.send({"Op":"apply", "Roid":roid, "Name":self.roles[roid], "Uid":player.uid})
        return True


    def acceptApply(self, player, roid):
        print "applyRole"
        if self.actors.get(roid) is not None:
            return False
        self.actors[roid] = player
        return True


    def enterPrepareStatus(self):
        print "enterPrepareStatus"
        if len(self.actors) != len(self.roles):
            self.room.cancelShow()
            return
        self.status = const.SHOW_STATUS_PREPARE
        bc = {"Op":"status", "Status":self.status, "Time":const.PREPARE_TIME}
        self.room.broadcast(bc)


    def enterStartStatus(self):
        print "enterStartStatus"
        self.status = const.SHOW_STATUS_START
        bc = {"Op":"status", "Status":self.status, "Time":const.SHOW_TIME}
        self.room.broadcast(bc)


    def update(self):
        print "show update"
        if self.status == const.SHOW_STATUS_APPLY:
            if time.time() - self.create_time >= const.APPLY_TIME: 
                self.enterPrepareStatus()
        elif self.status == const.SHOW_STATUS_PREPARE:
            if time.time() - self.create_time >= (const.APPLY_TIME + const.PREPARE_TIME): 
                self.enterStartStatus()


    def leave(self, player):
        if player == self.director:
            return self.room.cancelShow()

        for roid, actor in self.actors.items():
            if actor == player:
                del self.actors[roid]
                self.room.broadcast({"Op":"RoleLeave", "Roid":roid})

