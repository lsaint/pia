# -*- coding: utf-8 -*-

import time


timer_list = []

def setTimer(func, interval):
    def timer():
        while True:
            gevent.sleep(interval)
            func()
    timer_list.append(timer)

