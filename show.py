# -*- coding: utf-8 -*-

import const


class Show(object):

    def __init__(self, director, scid, name, roles):
        self.director = director
        self.scid = scid
        self.name = name
        self.roles = roles
        self.actors = {}
        self.status = const.SHOW_STATUS_RECRUIT


    def join(self, player, roid):
        pass



