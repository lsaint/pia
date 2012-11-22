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
        self.create_time = time.time()


    def applyRole(self, player, roid):
        print "applyRole"
        #self.applying[player] = roid
        if self.actors.get(roid) is not None:
            return False
        self.director.send({"Op":"apply", "Roid":roid, "Uid":player.uid})
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
        print "enterShowStatus"
        self.status = const.SHOW_STATUS_START
        bc = {"Op":"status", "Status":self.status}
        self.room.broadcast(bc)


    def update(self):
        print "show update"
        if self.status == const.SHOW_STATUS_APPLY:
            if time.time() - self.create_time >= const.APPLY_TIME: 
                self.enterPrepareStatus()
        if self.status == const.SHOW_STATUS_PREPARE:
            if time.time() - self.create_time >= (const.APPLY_TIME + const.PREPARE_TIME): 
                self.enterStartStatus()


