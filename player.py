# -*- coding: utf-8 -*-
import json

from const  import DELIMITER



class Player(object):

    def __init__(self, uid, name, room, s):
        self.room = room
        self.uid = uid
        self.name = name
        self.socket = s

    def send(self, msg):
        self.socket.sendall(json.dumps(msg) + DELIMITER)
        #print "send-msg", self.socket, msg



class Actor(object):

    def __init__(self, player, scid, roid):
        self.player = player
        self.scid = scid
        self.roid = roid



