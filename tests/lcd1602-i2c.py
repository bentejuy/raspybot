#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/lcd1602-i2c
# Purpose:
#
# Created:      01/27/2016
# Modified:     01/28/2016
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from __future__ import print_function

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time

from raspybot.devices.display import LiquidCrystal
from raspybot.io.interface import InterfaceManager, InterfaceI2CMaster, InterfaceI2CSlave

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# With I2C connection. The I2C address is 0x27 (default I2C address for PCA8574)

mgr = InterfaceManager()

ifm = InterfaceI2CMaster(mgr)
ifs = InterfaceI2CSlave(mgr, 0x27)

lcd = LiquidCrystal(ifs, LiquidCrystal.LCD2004A)

try:
    lcd.set_cursor(False)
    time.sleep(1.5)

    print("Printing characters...")
    for x in range(8):
        lcd.write(str(x), x * 2, 0)
        lcd.write(str(x + 1), x * 2, 1)

    time.sleep(2)

    lcd.clear()
    lcd.set_cursor(True)

    time.sleep(1.5)

    print("Printing text...")
    lcd.writeln("Connection with\n  I2C protocol")
    time.sleep(3)

    lcd.off()


except KeyboardInterrupt:
    pass

except Exception as error:
    print(error)

finally:
    mgr.delete(ifm)
    mgr.cleanup()