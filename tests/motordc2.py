#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/motordc2
# Purpose:      Test MotorDC in PWM_SIMPLE mode
#
# Author:       Bentejuy Lopez
# Created:      12/03/2015
# Modified:     12/09/2015
# Version:      0.0.07
# Copyright:    (c) 2015 Bentejuy Lopez
# Licence:      MIT
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from raspybot.devices.motor import MotorDC
from raspybot.io.interface import InterfaceManager, InterfaceGPIO, InterfacePWM

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def show_help():
    print "Testing MotorDC in PWM_SIMPLE mode"
    print " f : Move motor to right side"
    print " s : stop motor"
    print " + : increment the speed"
    print " - : decrement the speed"
    print " q : quit..."
    print " h : show this help\n\n"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface1 = InterfacePWM(manager, pinout=15)
motor1 = MotorDC(iface1, MotorDC.PWM_SIMPLE, name='Motor DC')

try:
    while True:
        cmd = raw_input('Enter command (h for help) : ')

        if cmd == 'f':
            motor1.forward(50)

        elif cmd == 's':
            motor1.stop()

        elif cmd == '+':
            motor1.speed_up(5)

        elif cmd == '-':
            motor1.speed_down(5)

        elif cmd == 'h':
            show_help()

        elif cmd == 'q':
            raise KeyboardInterrupt


except KeyboardInterrupt:
    print '\nScript stopped...'

except Exception, error:
    print error

finally:
    motor1.stop()

    manager.delete(iface1)
    manager.cleanup()
