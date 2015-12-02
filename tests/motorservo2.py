#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/servoservo2
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      10/25/2015
# Modified:     10/26/2015
# Version:      0.0.07
# Copyright:    (c) 2015 Bentejuy Lopez
# Licence:      MIT
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time

from raspybot.devices.button import Buttons
from raspybot.devices.motor import MotorServo
from raspybot.io.interface import InterfaceManager, InterfaceGPIO, InterfacePWM

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

BTN = (4, 14, 15, 17, 18)       # Defined a tuple with input channel (BCM mode)for the push buttons

BTN_MIDDLE, \
BTN_LEFT_SIDE, \
BTN_LEFT_QUARTER, \
BTN_RIGHT_SIDE, \
BTN_RIGHT_QUARTER  = BTN             # Sets the value to some variables

MIDDLE_SG90 = 180 / 2
MIDDLE_MG996 = 180 / 2

ONE_QUARTER_SG90 = 180 / 4
ONE_QUARTER_MG996 = 180 / 4

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def on_action(obj, channel, action):
    global servo1, servo2, servo3

#   print '"{}" receives the action "{}" in channel "{}"'.format(obj.get_name(), action, channel)

    if channel == BTN_MIDDLE:
        print "Mitad", channel, MIDDLE_MG996, MIDDLE_SG90

        servo1.angle_to(MIDDLE_MG996)
        servo2.angle_to(MIDDLE_SG90)
        servo3.angle_to(MIDDLE_MG996)

    elif channel == BTN_LEFT_QUARTER:
        print "1/4 Izquierda", channel, ONE_QUARTER_MG996, ONE_QUARTER_MG996

        servo1.angle_to(ONE_QUARTER_MG996)
        servo2.angle_to(ONE_QUARTER_SG90)
        servo3.angle_to(ONE_QUARTER_MG996)

    elif channel == BTN_LEFT_SIDE:
        print "Todo Izquierda", channel

        servo1.backward()
        servo2.backward()
        servo3.backward()

    elif channel == BTN_RIGHT_QUARTER:
        print "1/4 Derecha", channel, ONE_QUARTER_MG996 * 3, ONE_QUARTER_MG996 * 3

        servo1.angle_to(ONE_QUARTER_MG996 * 3)
        servo2.angle_to(ONE_QUARTER_SG90 * 3)
        servo3.angle_to(ONE_QUARTER_MG996 * 3)

    elif channel == BTN_RIGHT_SIDE:
        print "Todo Derecha", channel

        servo1.forward()
        servo2.forward()
        servo3.forward()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface1 = InterfaceGPIO(manager, pinin=(4, 14, 15, 17, 18))
iface2 = InterfacePWM(manager, pinout=13)
iface3 = InterfacePWM(manager, pinout=19)
iface4 = InterfacePWM(manager, pinout=26)

servo1 = MotorServo(iface2, (0.0002, 0.0024), (0, 180), 50, 0.19/60)        # Servo MG996R
servo2 = MotorServo(iface3, (0.0005, 0.0024), (0, 180), 50, 0.12/60)        # Servo SG90
servo3 = MotorServo(iface4, (0.0002, 0.0024), (0, 180), 50, 0.19/60)        # Servo MG996R

buttons = Buttons(iface1, clicked=on_action)

for pin in iface1.get_input_channels():
    buttons.setup(pin, buttons.CLICKED, buttons.PUD_UP, 500)


print 'Program started'
print 'Press CTRL-C to interrupt the program....'

servo1.angle_to(MIDDLE_MG996)
servo2.angle_to(MIDDLE_SG90)
servo3.angle_to(MIDDLE_MG996)


try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print '\nProgram stopped...'

    servo1.stop()
    servo2.stop()
    servo3.stop()

finally:
    manager.delete(iface1)
    manager.delete(iface2)
    manager.delete(iface3)
    manager.delete(iface4)

    manager.cleanup()
