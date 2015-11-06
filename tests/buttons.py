#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:          tests/buttons.py
# Purpose:
#
# Author:        Bentejuy Lopez
# Created:       05/01/2015
# Modified:      10/18/2015
# Version:       0.0.05
# Copyright:     (c) 2015 Bentejuy Lopez
# Licence:       MIT
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time

from raspybot.devices.button import Buttons
from raspybot.io.interface import InterfaceManager, InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def on_action(obj, channel, action):
    print '"{}" receives the action "{}" in channel "{}"'.format(obj.get_name(), action, channel)

    if channel == 4:
        print 'Action 1'
    elif channel == 14:
        print 'Action 2'
    elif channel == 17:
        print 'Action 3'
    else:
        print 'From where has come this channel => {} ?'.format(channel)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface = InterfaceGPIO(manager, pinin=(4, 14, 17, 18))
buttons = Buttons(iface, name='My Buttons Object', clicked=on_action, release=on_action)

buttons.setup(4, buttons.RELEASE, buttons.PUD_UP)
buttons.setup(14, buttons.CLICKED, buttons.PUD_UP)
buttons.setup(17, buttons.RELEASE, buttons.PUD_UP)
buttons.setup(18, buttons.CLICKED, buttons.PUD_UP)

print 'Program started'
print 'Press CTRL-C to interrupt the program....'

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print '\nProgram stopped...'

finally:
    manager.delete(iface)
    manager.cleanup()
