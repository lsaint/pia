# -*- coding: utf-8 -*-

from gevent.server import StreamServer


class AuthServer(object):

    def __init__(self):
        pass


    def start(self):
        print "Starting auth server on port 3333"
        server = StreamServer(('0.0.0.0', 3333), self.accept)
        server.serve_forever()


    def accept(self, socket, address):
        line = socket.recv(1024)
        socket.sendall("""<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>\0""")


