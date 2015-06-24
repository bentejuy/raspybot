#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:          tests/flipflop.py
# Purpose:
#
# Author:        Bentejuy Lopez
# Created:       05/04/2015
# Modified:      05/04/2015
# Version:       0.0.03
# Copyright:     (c) 2015 Bentejuy Lopez
# Licence:       MIT
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import sys
import time
import logging

from raspybot.devices.logic import FlipFlop
from raspybot.devices.button import Buttons
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


def on_action(obj, channel, action):
    global index, flipflop

    if channel == 4:
        flipflop.toggle()
        print  'Toggle all channels in flipflop'

    elif channel == 14:
        if flipflop.get() & (1 << index):
            flipflop.reset(index)
            print 'Reset the channel number {}'.format(index)

        else:
            flipflop.set(index)
            print 'Set the channel number {}'.format(index)

        if index >= 7:
            index = 0
        else:
            index += 1

        print index, bin(flipflop.get())

    elif channel == 17:
        index = 0
        flipflop.set()
        print 'Set to 1 all channels in flipflop'

    else:
        index = 0
        flipflop.reset()
        print 'Reset to 0 all channels in flipflop'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

index = 0
manager = InterfaceManager()

iface1 = InterfaceGPIO(manager, pinin=(4, 14, 17, 18))
iface2 = InterfaceGPIO(manager, pinout=(9, 25, 11, 8, 19, 16, 26, 20))

buttons = Buttons(iface1, 'Buttons Object', release=on_action)
flipflop = FlipFlop(iface2, 'FlipFlop Object')

buttons.setup(4, buttons.RELEASE, buttons.PUD_UP)
buttons.setup(14, buttons.RELEASE, buttons.PUD_UP)
buttons.setup(17, buttons.RELEASE, buttons.PUD_UP)
buttons.setup(18, buttons.RELEASE, buttons.PUD_UP)

print 'Program started.'
print 'Press CTRL-C to interrupt the program....'

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print '\nProgram stopped...'

finally:
    manager.cleanup()
