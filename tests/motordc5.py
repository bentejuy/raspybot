#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/motordc5
# Purpose:      Test MotorDC in ADV_REVERSIBLE mode
#
# Created:      12/04/2015
# Modified:     12/17/2015
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from __future__ import ( print_function )

from raspybot.devices.motor import MotorDC
from raspybot.io.interface import InterfaceManager, InterfaceGPIO, InterfacePWM

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def show_help():
    print('Testing MotorDC in ADV_REVERSIBLE mode')
    print(' f : Move motor to right side')
    print(' b : Move motor to left side')
    print(' + : increment the speed')
    print(' - : decrement the speed')
    print(' s : stop motor')
    print(' q : quit...')
    print(' h : show this help\n\n')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

manager = InterfaceManager()

iface1 = InterfacePWM(manager, pinout=14)
iface2 = InterfaceGPIO(manager, pinout=(15, 18))
motor1 = MotorDC((iface1, iface2), MotorDC.ADV_REVERSIBLE, name='Motor DC')

try:
    while True:
        cmd = raw_input('Enter command (h for help) : ')

        if cmd == 'f':
            motor1.forward()

        elif cmd == 'b':
            motor1.backward()

        elif cmd == '+':
            motor1.speed_up(5)

        elif cmd == '-':
            motor1.speed_down(5)

        elif cmd == 's':
            motor1.stop()

        elif cmd == 'h':
            show_help()

        elif cmd == 'q':
            raise KeyboardInterrupt


except KeyboardInterrupt:
    print('\nScript stopped...')

except Exception as error:
    print('Error :', error)

finally:
    motor1.stop()

    manager.delete(iface1)
    manager.delete(iface2)
    manager.cleanup()

