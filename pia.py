# -*- coding: utf-8 -*-

import gevent

from authserver import AuthServer
from piaserver  import PiaServer
from piamgr     import PiaMgr


if __name__ == '__main__':
    pmgr = PiaMgr()
    srv = PiaServer(pmgr)
    aut = AuthServer()

    jobs = [gevent.spawn(srv.start), gevent.spawn(aut.start)]
    gevent.joinall(jobs)


