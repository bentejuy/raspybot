#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/servoservo2
# Purpose:
#
# Created:      10/25/2015
# Modified:     12/17/2015
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time

from __future__ import print_function

from raspybot.devices.button import Buttons
from raspybot.devices.motor import MotorServo
from raspybot.io.interface import InterfaceManager, InterfaceGPIO, InterfacePWM

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Defined a tuple with input channel (BCM mode) for the push buttons
BTNS = (4, 14, 15, 17, 18)

# Input channels is assigned to constants for easy identification
BTN_MIDDLE, \
BTN_LEFT_SIDE, \
BTN_LEFT_QUARTER, \
BTN_RIGHT_SIDE, \
BTN_RIGHT_QUARTER  = BTNS

# Angles for Servo SG90
SG90_MIN_ANGLE = 0
SG90_MAX_ANGLE = 180
SG90_HALF_ANGLE = (abs(SG90_MAX_ANGLE) - abs(SG90_MIN_ANGLE)) / 4

# Angles for Servo MG996R
MG996R_MIN_ANGLE = 0
MG996R_MAX_ANGLE = 270
MG996R_HALF_ANGLE = (abs(MG996R_MAX_ANGLE) - abs(MG996R_MIN_ANGLE)) / 4

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def on_action(obj, channel, action):
    global servo1, servo2, servo3

    if channel == BTN_MIDDLE:
        print('Moving to middle position =>', channel, MG996R_HALF_ANGLE * 2, SG90_HALF_ANGLE * 2)

        servo1.angle_to(MG996R_HALF_ANGLE * 2)
        servo2.angle_to(SG90_HALF_ANGLE * 2)
        servo3.angle_to(MG996R_HALF_ANGLE * 2)

    elif channel == BTN_LEFT_QUARTER:
        print('Moving 1/4 Left Side =>', channel, MG996R_HALF_ANGLE, MG996R_HALF_ANGLE)

        servo1.angle_to(MG996R_HALF_ANGLE)
        servo2.angle_to(SG90_HALF_ANGLE)
        servo3.angle_to(MG996R_HALF_ANGLE)

    elif channel == BTN_LEFT_SIDE:
        print('Moving to Left Side =>', channel, MG996R_MIN_ANGLE, SG90_MIN_ANGLE)

        servo1.backward()
        servo2.backward()
        servo3.backward()

    elif channel == BTN_RIGHT_QUARTER:
        print('Moving 1/4 Right Side =>', channel, MG996R_HALF_ANGLE * 3, SG90_HALF_ANGLE * 3)

        servo1.angle_to(MG996R_HALF_ANGLE * 3)
        servo2.angle_to(SG90_HALF_ANGLE * 3)
        servo3.angle_to(MG996R_HALF_ANGLE * 3)

    elif channel == BTN_RIGHT_SIDE:
        print('Moving to Right Side =>', channel, MG996R_MAX_ANGLE, SG90_MAX_ANGLE)

        servo1.forward()
        servo2.forward()
        servo3.forward()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface1 = InterfaceGPIO(manager, pinin=BTNS)
iface2 = InterfacePWM(manager, pinout=13)
iface3 = InterfacePWM(manager, pinout=19)
iface4 = InterfacePWM(manager, pinout=26)

servo1 = MotorServo(iface2, (0.0002, 0.0024), (MG996R_MIN_ANGLE, MG996R_MAX_ANGLE), 50, 0.22/60)        # Servo MG996R
servo2 = MotorServo(iface3, (0.0005, 0.0024), (SG90_MIN_ANGLE, SG90_MAX_ANGLE), 50, 0.12/60)            # Servo SG90
servo3 = MotorServo(iface4, (0.0002, 0.0024), (MG996R_MIN_ANGLE, MG996R_MAX_ANGLE), 50, 0.22/60)        # Servo MG996R

buttons = Buttons(iface1, clicked=on_action)

for pin in iface1.get_input_channels():
    buttons.setup(pin, buttons.CLICKED, buttons.PUD_UP, 500)


print('Program started')
print('Press CTRL-C to interrupt the program....')

servo1.angle_to(MG996R_MIN_ANGLE)
servo2.angle_to(SG90_MIN_ANGLE)
servo3.angle_to(MG996R_MIN_ANGLE)


try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print('\nProgram stopped...')

    servo1.stop()
    servo2.stop()
    servo3.stop()

finally:
    manager.delete(iface1)
    manager.delete(iface2)
    manager.delete(iface3)
    manager.delete(iface4)

    manager.cleanup()
