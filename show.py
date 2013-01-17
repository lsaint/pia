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
        #remain_time = 0
        t = int(time.time()) - self.create_time
        if const.APPLY_TIME > t:
            t = const.APPLY_TIME - t
        #if t > const.APPLY_TIME:
        #    t -= const.APPLY_TIME
        #    remain_time = const.PREPARE_TIME - t
        #if t > const.PREPARE_TIME:
        #    t -= const.PREPARE_TIME
        #    remain_time = const.SHOW_TIME - t
        #else:
        #    remain_time = const.APPLY_TIME - t

        return {"Director":self.director.uid,\
                "Scid":self.scid,
                "Name":self.name,
                "Roles":self.roles,
                "Actor":self.actors,
                "Status":self.status,
                "Time":t}


    def applyRole(self, player, roid):
        print "applyRole"
        #self.applying[player] = roid
        if self.actors.get(roid) is not None:
            return False
        self.director.send({"Op":"apply", "Roid":roid, "Name":self.roles[roid], "Uid":player.uid})
        return True


    def acceptApply(self, uid, roid):
        print "applyRole", roid, uid
        if self.actors.get(roid) is not None:
            return False
        self.actors[roid] = uid
        if len(self.actors) == len(self.roles):
            self.enterPrepareStatus()
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
        if self.status == const.SHOW_STATUS_APPLY:
            if time.time() - self.create_time >= const.APPLY_TIME: 
                self.enterPrepareStatus()
        elif self.status == const.SHOW_STATUS_PREPARE:
            if time.time() - self.create_time >= (const.APPLY_TIME + const.PREPARE_TIME): 
                self.enterStartStatus()
        elif self.status == const.SHOW_STATUS_START:
            #if time.time() - self.create_time >= (const.APPLY_TIME + const.PREPARE_TIME + const.SHOW_TIME):
            #    self.room.cancelShow()
            pass


    def leave(self, player):
        if player == self.director:
            return self.room.cancelShow()

        for roid, actor in self.actors.items():
            if actor == player.uid:
                del self.actors[roid]
                self.room.broadcast({"Op":"RoleLeave", "Roid":roid})

