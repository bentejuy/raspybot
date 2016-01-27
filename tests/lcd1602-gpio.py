#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/lcd1602-direct
# Purpose:
#
# Created:      01/27/2016
# Modified:     01/27/2016
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from __future__ import print_function

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time

from raspybot.devices.display import LiquidCrystal
from raspybot.io.interface import InterfaceManager, InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# With direct connection. The correspondence of the pins between the
# InterfaceGPIO and the LCD is in this order: RS, RW, EN, D4 to D7

mgr = InterfaceManager()

ifc = InterfaceGPIO(mgr, pinout=(17, 27, 22, 26, 19, 13, 6))
lcd = LiquidCrystal(ifc, LiquidCrystal.LCD1602A)

try:
    lcd.set_cursor(False)
    time.sleep(1.5)

    print("Printing characters...")
    for x in range(8):
        lcd.write(str(x), x * 2, 0)
        lcd.write(str(x + 1), x * 2, 1)

    time.sleep(2)

    lcd.home()
    lcd.clear()
    lcd.set_cursor(True)

    time.sleep(1.5)

    print("Printing text...")
    lcd.writeln("Direct connection\n   to LCD1604")
    time.sleep(3)

    lcd.off()

except KeyboardInterrupt:
    pass

except Exception as error:
    print(error)

finally:
    mgr.delete(ifc)
    mgr.cleanup()