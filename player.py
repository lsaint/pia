# -*- coding: utf-8 -*-
import json

from const  import DELIMITER



class Player(object):

    def __init__(self, uid, name, room, s):
        self.room = room
        self.uid = uid
        self.name = name
        self.socket = s

    def send(self, dt):
        self.socket.send(json.dumps(dt) + DELIMITER)

