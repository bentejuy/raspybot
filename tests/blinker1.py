#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:          tests/blinker1
# Purpose:
#
# Author:        Bentejuy Lopez
# Created:       04/02/2015
# Modified:      10/18/2015
# Version:       0.0.05
# Copyright:     (c) 2015 Bentejuy Lopez
# Licence:       MIT
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import sys
import time
import logging

from raspybot.devices.logic import Blinker
from raspybot.io.interface import InterfaceManager, InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def logger_init(debug=None):
    log = logging.getLogger('')

    hld = logging.StreamHandler(sys.stdout)
    hld.setLevel(debug and logging.DEBUG or logging.WARNING)
    hld.setFormatter(logging.Formatter('%(levelname)s :: %(name)s [%(lineno)d] --> %(message)s'))
    log.addHandler(hld)

    log.setLevel(debug and logging.DEBUG or logging.WARNING)

    return log

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logger_init(True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def startinfo(dev):
    logger.debug("Starting => {}".format(dev))


def stopinfo(dev):
    logger.debug("Stopping => {}".format(dev))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


manager = InterfaceManager()

iface = InterfaceGPIO(manager, pinout=(9, 25, 8, 11, 19, 16, 26, 20))
blinker = Blinker(iface, 'Blinker Test 1', delay=0.3, initial=0b10000001, start=startinfo, stop=stopinfo)

try:
    blinker.start()

    for x in xrange(50):
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
    blinker.stop()

finally:
    manager.delete(iface)
    manager.cleanup()
