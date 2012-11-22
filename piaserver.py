# -*- coding: utf-8 -*-

import json

from gevent.server import StreamServer

from piamgr import PiaMgr
from const  import DELIMITER


class PiaServer(object):

    def __init__(self, piaMgr):
        self.piaMgr = piaMgr


    def accept(self, socket, address):
        print 'New connection from %s:%s' % address
        fileobj = socket.makefile()
        while True:
            try:
                line = fileobj.readline()
            except Exception, e:
                print e
                self.piaMgr.disconnect(socket)
                break
            if not line:
                print ("client disconnected")
                self.piaMgr.disconnect(socket)
                break
            print "line", line
            jn = json.loads(line)
            if type(jn) == dict:
                self.dispatch(jn, socket)


    def dispatch(self, jn, socket):
        print "req", jn
        if jn["Op"] == "Login":
            self.piaMgr.onLogin(socket, **jn)
        else:
            self.piaMgr.commonCheck(socket, **jn)


    def start(self):
        print "Starting pia server on port 2222"
        server = StreamServer(('0.0.0.0', 2222), self.accept)
        server.serve_forever()


#if __name__ == '__main__':
#    srv = PiaServer(PiaMgr())
#    srv.start()

