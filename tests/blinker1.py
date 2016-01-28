#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:          tests/blinker1
# Purpose:
#
# Created:       04/02/2015
# Modified:      01/28/2016
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from __future__ import print_function

import sys
import time

from raspybot.devices.logic import Blinker
from raspybot.io.interface import InterfaceManager, InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def startinfo(dev):
    print('Starting => {}'.format(dev))


def stopinfo(dev):
    print('Stopping => {}'.format(dev))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface = InterfaceGPIO(manager, pinout=(9, 25, 8, 11, 19, 16, 26, 20))
blinker = Blinker(iface, 'Blinker Test 1', delay=0.3, initial=0b10000001, start=startinfo, stop=stopinfo)

try:
    blinker.start()

    for x in range(50):
        if x == 10:
            blinker.stop()
            blinker.set_value(0b00001111)
            blinker.start()

        if x == 20:
            blinker.stop()
            blinker.set_value(0b01010101)
            blinker.start()

        if x == 30:
            blinker.stop()
            blinker.set_value(0b11011011)
            blinker.start()

        if x == 40:
            blinker.stop()
            blinker.set_value(0b11000011)
            blinker.start()

        time.sleep(1.5)

except KeyboardInterrupt:
    pass

finally:
    blinker.stop()

    manager.delete(iface)
    manager.cleanup()
