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
        buf = ""
        while True:
            try:
                buf =  "%s%s" % (buf, socket.recv(1024))
            except Exception, e:
                print e
                break
            if not buf:
                break
            print "buf", buf
            if DELIMITER not in buf:
                continue
            la = buf.rindex(DELIMITER)
            buf, lines = buf[la+1:], buf[:la]
            lt = lines.splitlines()
            for line in lt:
                jn = json.loads(line)
                if type(jn) == dict:
                    self.dispatch(jn, socket)


    def dispatch(self, jn, socket):
        print "req", jn
        method = getattr(self.piaMgr, jn["Op"])
        method(socket, **jn)


    def start(self):
        print "Starting pia server on port 2222"
        server = StreamServer(('0.0.0.0', 2222), self.accept)
        server.serve_forever()


#if __name__ == '__main__':
#    srv = PiaServer(PiaMgr())
#    srv.start()

