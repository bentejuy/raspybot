#!/usr/bin/env python
# -+- coding: utf-8 -+-

from __future__ import print_function

import time

from raspybot.devices.sensor import BMP180
from raspybot.io.interface import InterfaceManager, InterfaceI2CMaster, InterfaceI2CSlave

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

mgr = InterfaceManager()

ifm = InterfaceI2CMaster(mgr)
ifs = InterfaceI2CSlave(mgr, 0x77)

bmp = BMP180(ifs)

try:
    while True:
        bmp.update(True, True)
        time.sleep(0.1)
        print("Temperature\t: {0} C\nPressure\t: {1} Pa\nAltitude\t: {2}m".format(bmp.get_temperature(), bmp.get_pressure(), bmp.get_altitude(1027)))
        time.sleep(1.5)

except KeyboardInterrupt:
    pass

except Exception as error:
    print(error)

finally:
    mgr.delete(ifm)
    mgr.cleanup()
