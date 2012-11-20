# -*- coding: utf-8 -*-

from gevent.server import StreamServer


class AuthServer(object):

    def __init__(self):
        pass


    def start(self):
        print "Starting auth server on port 22222"
        server = StreamServer(('0.0.0.0', 22222), self.accept)
        server.serve_forever()


    def accept(self, socket, address):
        socket.send("""<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>\0""")

