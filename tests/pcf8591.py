#!/usr/bin/env python
# -+- coding: utf-8 -+-

from __future__ import print_function

import time

from raspybot.devices.analogic import PCF8591
from raspybot.io.interface import InterfaceManager, InterfaceI2CMaster, InterfaceI2CSlave

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

mgr = InterfaceManager()

ifm = InterfaceI2CMaster(mgr)
ifs = InterfaceI2CSlave(mgr, 0x48)

adc = PCF8591(ifs)

try:

    print("Reading inputs...")

    for i in range(5):
        print("Input 0 :{}\nInput 1 :{}\nInput 2 :{}\nInput 2 :{}\n".format(adc.read(0), adc.read(1), adc.read(2), adc.read(3)))
        time.sleep(1)


    print("Writing sawtooth wave...")

    for i in range(50):
        for sawtooth_wave in range(256):
            adc.write(sawtooth_wave)

    time.sleep(1.5)

    print("Writing triangular wave...")

    for i in range(50):
        triangular_wave = range(256)
        triangular_wave.extend(range(254, -1, -1))

        adc.write(triangular_wave)

    time.sleep(1.5)

    adc.write(0)
    adc.disableDAC()


except KeyboardInterrupt:
    pass

except Exception as error:
    print(error)

finally:
    mgr.delete(ifm)
    mgr.cleanup()
