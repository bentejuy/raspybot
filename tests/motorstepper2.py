#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/motorstepper2
# Purpose:      Testing MotorStepperUnipolar object with mode not blocking
#
# Created:      04/01/2015
# Modified:     12/05/2015
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


from __future__ import print_function

import sys
import time

from raspybot.devices.motor import MotorStepperUnipolar
from raspybot.io.interface import InterfaceManager, InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def startinfo(motor):
    print('Starting Motor =>', motor.get_name())


def stopinfo(motor):
    print('Stopping Motor =>', motor.get_name())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface1 = InterfaceGPIO(manager, pinout=(17, 18, 22, 23))
iface2 = InterfaceGPIO(manager, pinout=(9, 25, 11, 8))

motor1 = MotorStepperUnipolar(iface1, 'Motor 1', start=startinfo, stop=stopinfo)
motor2 = MotorStepperUnipolar(iface2, 'Motor 2', start=startinfo, stop=stopinfo)

try:
    motor1.set_mode(motor1.MODE_SINGLE)
    motor1.set_degrees(5.625/64)                #  Default degreess by step for stepper motor 28BYJ-48
    motor1.set_speed(15)

    motor2.set_mode(motor2.MODE_DUAL)
    motor2.set_degrees(5.625/64)                #  Default degreess by step for stepper motor 28BYJ-48
    motor2.set_speed(15)

    count = 5

    while count:
        if not motor1.alive() and not motor2.alive():
            print('Running...', count)

            if count % 2:
                motor1.forward(degrees=180)
                motor2.forward(degrees=180)
            else:
                motor1.backward(degrees=180)
                motor2.backward(degrees=180)

            count -= 1

        time.sleep(0.5)

    time.sleep(1.5)

    for angle in (-90, 180, -180, 180, -90):
        motor1.angle_to(angle)
        motor2.angle_to(angle)

        while motor1.alive() and motor2.alive():
            time.sleep(1)

except KeyboardInterrupt:
    print('\nScript stopped...')

except Exception as error:
    print('Error :', error)

finally:
    motor1.stop()
    motor2.stop()

    manager.delete(iface1)
    manager.delete(iface2)
    manager.cleanup()
