#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/motorstepper1
# Purpose:      Testing MotorStepperUnipolar object with blocking mode
#
# Author:       Bentejuy Lopez
# Created:      03/20/2015
# Modified:     03/22/2015
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

iface1 = InterfaceGPIO(manager, pinout=(17, 18, 22, 23))
iface2 = InterfaceGPIO(manager, pinout=(9, 25, 11, 8))


motor1 = MotorStepperUnipolar(iface1, 'Motor stepper 1', start=startinfo, stop=stopinfo)
motor2 = MotorStepperUnipolar(iface2, 'Motor stepper 2', start=startinfo, stop=stopinfo)

try:
    motor1.set_mode(motor1.MODE_HALF)
    motor1.set_degrees(5.625/64)                    #  Default steps for stepper motor 28BYJ-48
    motor1.set_speed(20)

    motor2.set_mode(motor2.MODE_DUAL)
    motor2.set_degrees(5.625/64)                    #  Default steps for stepper motor 28BYJ-48
    motor2.set_speed(20)

    motor1.forward(degrees=360)
    motor2.forward(degrees=360)

    motor1.join()
    motor2.join()

    time.sleep(0.5)

    motor1.backward(2048)                           # Move 2048 steps
    motor2.backward(2048)

    motor1.join()
    motor2.join()

    time.sleep(0.5)

    motor1.angle_to(180)                             # Turn clockwise 180 degrees
    motor2.angle_to(180)

    motor1.join()
    motor2.join()

    time.sleep(0.5)

    motor1.angle_to(-180)                            # Turn counteclockwise 180 degrees
    motor2.angle_to(-180)

    motor1.join()
    motor2.join()


except KeyboardInterrupt:
    logger.info('Script stopped...')

except Exception, error:
    logger.error(error)

finally:
    motor1.stop()
    motor2.stop()

    manager.cleanup()

