#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:          tests/blinker2
# Purpose:
# Created:       04/03/2015
# Modified:      01/28/2016
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from __future__ import print_function

import time
import random

from raspybot.devices.logic import Blinker
from raspybot.io.interface import InterfaceManager, InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def startinfo(dev):
    print('Starting => {}'.format(dev))


def stopinfo(dev):
    print('Stopping => {}'.format(dev))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

flag = False

def do_random(value, count):
    return random.randint(0x00, 0xFF)


def do_shift2left(value, count):
    if value < 128:
        return value << 1
    else:
        return 1


def do_shift2right(value, count):
    if value:
        return value >> 1
    else:
        return 128


def do_pingpong(value, count):
    global flag

    if flag:
        flag = value > 2
        return value >> 1
    else:
        flag = value >= 64
        return value << 1


# For more info see : https://www.youtube.com/watch?v=wAoKzfbGnCc
def do_kitt(value, count):
    global flag

    if flag:
        flag = value > 7
        return value >> 1
    else:
        flag = value >= 96
        return value << 1


def do_vumeter(value, count):
    x = (0, 24, 60, 126, 255)

    if value == 0:
        return 24
    elif value == 255:
        return 126
    else:
        return x[x.index(value) + (random.randint(0, 1) and 1 or -1)]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface = InterfaceGPIO(manager, pinout=(9, 25, 11, 8, 19, 16, 26, 20))
blinker = Blinker(iface, 'Blinker Test 2', delay=.1, checker=do_random, start=startinfo, stop=stopinfo)

try:
    blinker.start()

    for x in range(60):
        if x == 10:
            blinker.stop()
            blinker.set_value(1)
            blinker.set_callback(do_shift2left)
            blinker.start()

        if x == 20:
            blinker.stop()
            blinker.set_value(128)
            blinker.set_callback(do_shift2right)
            blinker.start()

        if x == 30:
            flag = False
            blinker.stop()
            blinker.set_value(1)
            blinker.set_callback(do_pingpong)
            blinker.start()

        if x == 40:
            flag = False
            blinker.stop()
            blinker.set_value(3)
            blinker.set_callback(do_kitt)
            blinker.start()

        if x == 50:
            flag = False
            blinker.stop()
            blinker.set_value(0)
            blinker.set_callback(do_vumeter)
            blinker.start()

        time.sleep(1.5)

except KeyboardInterrupt:
    pass

finally:
    blinker.stop()

    manager.delete(iface)
    manager.cleanup()
