# -*- coding: utf-8 -*-

import time

import const

###

class Timer(object):

    tid = 0

    def __init__(self):
        self.timers = {}


    def settimer(self, interval, func):
        self.tid += 1
        self.timers[self.tid] = (interval, time.time(), func)
        return self.tid


    def update(self):
        now = time.time()
        for tid, timer in self.timers.items():
            interval, last, func = timer
            if now - last >= interval:
                self.timers[tid] = (interval, now, func)
                func()



### 


class Show(Timer):

    def __init__(self, director, scid, name, roles):
        Timer.__init__(self)
        self.director = director
        self.room = director.room
        self.scid = scid
        self.name = name
        self.roles = roles
        self.actors = {} # {roid:uid}
        self.gid2price = {}
        self.uid2price = {}
        self.status = const.SHOW_STATUS_APPLY
        self.enter_status_time = int(time.time())

        self.settimer(3, self.broadcastGiftInfo)


    def getShowInfo(self):
        t = int(time.time()) - self.enter_status_time
        return {"Director":self.director.uid,\
                "Scid":self.scid,
                "Name":self.name,
                "Roles":self.roles,
                "Actor":self.actors,
                "Status":self.status,
                "Time":t}


    def applyRole(self, player, roid):
        print "applyRole"
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


    def setActorGiftPrice(self, uid, price):
        self.uid2price[uid] = price


    def enterPrepareStatus(self):
        print "enterPrepareStatus"
        self.enter_status_time = int(time.time())
        if len(self.actors) != len(self.roles):
            self.room.cancelShow()
            return
        self.status = const.SHOW_STATUS_PREPARE
        bc = {"Op":"status", "Status":self.status, "Time":const.PREPARE_TIME}
        self.room.broadcast(bc)


    def enterStartStatus(self):
        print "enterStartStatus"
        self.enter_status_time = int(time.time())
        self.status = const.SHOW_STATUS_START
        bc = {"Op":"status", "Status":self.status, "Time":const.SHOW_TIME}
        self.room.broadcast(bc)


    def update(self):
        Timer.update(self)
        if self.status == const.SHOW_STATUS_APPLY:
            if time.time() - self.enter_status_time >= const.APPLY_TIME: 
                self.enterPrepareStatus()
        elif self.status == const.SHOW_STATUS_PREPARE:
            if time.time() - self.enter_status_time >= const.PREPARE_TIME:
                self.enterStartStatus()
        elif self.status == const.SHOW_STATUS_START:
            pass


    def leave(self, player):
        if player == self.director:
            return self.room.cancelShow()

        for roid, actor in self.actors.items():
            if actor == player.uid:
                del self.actors[roid]
                self.room.broadcast({"Op":"RoleLeave", "Roid":roid})

        if self.uid2price.get(player.uid):
            del self.uid2price[player.uid]


    def onGiveGift(self, touid, gid, price):
        t = self.gid2price.get(gid) or 0
        self.gid2price[gid] = price + t

        if self.uid2price.get(touid) is None:
            self.uid2price[touid] = {gid:price}
        else:
            t = self.uid2price[touid].get(gid) or 0 
            self.uid2price[touid][gid] = price + t


    def broadcastGiftInfo(self):
        if len(self.uid2price) != 0:
            self.room.broadcast({"Op":"GiftInfo", "G":self.gid2price, "U":self.uid2price})


