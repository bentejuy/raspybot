#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/motorstepper2
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      04/01/2015
# Modified:     04/01/2015
# Version:      0.0.07
# Copyright:    (c) 2015 Bentejuy Lopez
# Licence:      MIT
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import sys
import time
import logging

from raspybot.devices.motor import MotorStepperUnipolar
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

iface1 = InterfaceGPIO(manager, pinout=(17,18,22,23))
iface2 = InterfaceGPIO(manager, pinout=(16,19,20,26))

motor1 = MotorStepperUnipolar(iface1, 'Motor 1', start=startinfo, stop=stopinfo)
motor2 = MotorStepperUnipolar(iface2, 'Motor 2', start=startinfo, stop=stopinfo)

try:
    motor1.set_mode(motor1.MODE_SINGLE)
    motor1.set_degrees(5.625/64)                #  Default steps for stepper motor 28BYJ-48
#   motor1.set_speed(5)

    motor2.set_mode(motor2.MODE_HALF)
    motor2.set_degrees(5.625/64)                #  Default steps for stepper motor 28BYJ-48
#   motor2.set_speed(5)

    motor1.forward(steps=1024)
    motor1.backward(steps=1024)

    count = 10

    while count:
        if not motor1.alive() and not motor2.alive():
            print "Running...", count

            if count % 2:
                motor1.forward(degrees=180)
                motor2.forward(degrees=180)
            else:
                motor1.backward(degrees=180)
                motor2.backward(degrees=180)

            count -= 1

        time.sleep(10)

except KeyboardInterrupt:
    logger.info('Script stopped...')

except Exception, error:
    logger.error(error)

finally:
    motor1.stop()
    motor2.stop()

    manager.cleanup()

