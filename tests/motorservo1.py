#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/motorservo1
# Purpose:
#
# Created:      03/27/2015
# Modified:     12/17/2015
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time

from __future__ import print_function

from raspybot.devices.motor import MotorServo
from raspybot.io.interface import InterfaceManager, InterfacePWM

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Angles for Servo 9G
SG90_MIN_ANGLE = 0
SG90_MAX_ANGLE = 180
SG90_HALF_ANGLE = (abs(SG90_MAX_ANGLE) - abs(SG90_MIN_ANGLE)) / 4

# Angles for Servo MG 996R
MG996R_MIN_ANGLE = 0
MG996R_MAX_ANGLE = 270
MG996R_HALF_ANGLE = (abs(MG996R_MAX_ANGLE) - abs(MG996R_MIN_ANGLE)) / 4

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def startinfo(motor):
    print('\tStarting Motor =>', motor.get_name())


def stopinfo(motor):
    print('\tStopping Motor =>', motor.get_name())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface1 = InterfacePWM(manager, pinout=5)
iface2 = InterfacePWM(manager, pinout=13)

servo1 = MotorServo(iface1, (0.0005, 0.0024), (SG90_MIN_ANGLE, SG90_MAX_ANGLE), 50, 0.16/60, 'Servo SG90', start=startinfo, stop=stopinfo)      # Servo SG90
servo2 = MotorServo(iface2, (0.0002, 0.0024), (MG996R_MIN_ANGLE, MG996R_MAX_ANGLE), 50, 0.22/60, 'Servo MG996R', start=startinfo, stop=stopinfo)    # Servo MG996R

try:
    count = 5

    while count:
        if not servo1.alive() and not servo2.alive():
            print('Running...', count)

            if count % 2:
                servo1.forward()
                servo2.forward()
            else:
                servo1.backward()
                servo2.backward()

            count -= 1

        time.sleep(3)


    for x in xrange(20):
        print('Moving Servo 1 to', (x % 5) * SG90_HALF_ANGLE, 'degrees')
        print('Moving Servo 2 to', (x % 5) * MG996R_HALF_ANGLE, 'degrees')

        servo1.angle_to((x % 5) * SG90_HALF_ANGLE)
        servo2.angle_to((x % 5) * MG996R_HALF_ANGLE)

        time.sleep(3)

except KeyboardInterrupt:
    servo1.stop()
    servo2.stop()

finally:
    manager.delete(iface1)
    manager.delete(iface2)

    manager.cleanup()
