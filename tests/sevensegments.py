#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/sevensegments
# Purpose:      testing sevensegment object in direct mode.
#
# Created:      11/24/2015
# Modified:     12/05/2015
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import sys
import time

from raspybot.devices.display import SevenSegment
from raspybot.io.interface import InterfaceManager, InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()
iface = InterfaceGPIO(manager, pinout=(5, 6, 13, 19, 26, 21, 20, 16))   # 8 pins for 7 segment and dot led in this order a,b,c,d,e,f,g and dp

display = SevenSegment(iface, SevenSegment.DIRECT_MODE)

try:
    for x in range(16):
        display.set(x)
        time.sleep(0.5)
        display.dot(True)
        time.sleep(0.5)
        display.dot(False)
        time.sleep(0.5)

except KeyboardInterrupt:
    print "\nProgram stopped..."

finally:
    manager.delete(iface)
    manager.cleanup()
