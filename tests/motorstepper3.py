#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/motorstepper3
# Purpose:      Testing MotorStepperBipolar object with InterfaceGPIO
#
# Author:       Bentejuy Lopez
# Created:      07/13/2015
# Modified:     10/18/2015
# Version:      0.0.09
# Copyright:    (c) 2015 Bentejuy Lopez
# Licence:      MIT
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import sys
import time
import logging

from raspybot.devices.motor import MotorStepperBipolar
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


def startinfo(motor):
    logger.debug("Starting Motor => %s" % motor.get_name())


def stopinfo(motor):
    logger.debug("Stopping Motor => %s" % motor.get_name())


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface1 = InterfaceGPIO(manager, pinout=(16, 19, 20, 26))
motor1 = MotorStepperBipolar(iface1, 'Motor 1', start=startinfo, stop=stopinfo)


try:
    motor1.set_degrees(7.5)                #  Default degreess by step for stepper motor KP54FP8-755
    motor1.set_speed(5)

    motor1.forward(48)
    motor1.join()

    time.sleep(0.5)

    motor1.backward(48)
    motor1.join()

    motor1.set_speed(30)

    count = 5

    while count:
        if not motor1.alive():
            print "Running...", count

            if count % 2:
                motor1.forward(degrees=180)
            else:
                motor1.backward(degrees=180)

            count -= 1

        time.sleep(0.5)

    motor1.join()


except KeyboardInterrupt:
    logger.info('Script stopped...')

except Exception, error:
    logger.error(error)

finally:
    motor1.stop()

    manager.delete(iface1)
    manager.cleanup()

