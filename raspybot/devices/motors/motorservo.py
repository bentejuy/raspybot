#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         MotorServo
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/27/2015
# Modified:     11/29/2015
# Version:      0.0.43
# Copyright:    (c) 2015-2016 Bentejuy Lopez
# Licence:      GLPv3
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""

    For more info see : https://www.youtube.com/watch?v=ddlDgUymbxc

"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from ..motor import Worker
from ..motor import MotorBase
from ..motor import InvalidTypeError, OutRangeError, IsRunningError, InvalidRangeError, MinMaxValueError, InterfaceNoSupported

from ..motor import InterfacePWM

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class MotorServo
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class MotorServo(MotorBase):
    def __init__(self, iface, pulses, angles, frequency=50, speed=None, name=None, start=None, stop=None):

        if not isinstance(iface, InterfacePWM):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        super(MotorServo, self).__init__(iface, name, start, stop)

        self._speed  = 0.02
        self._pulses = [None, None]
        self._angles = [None, None]
        self._frequency = None

        self._worker =  Worker(self.__run__)

        if not isinstance(pulses, (tuple, list)) or len(pulses) != 2:
            raise InvalidRangeError('pulses')

        if not isinstance(angles, (tuple, list)) or len(angles) != 2:
            raise InvalidRangeError('angles')

        if speed:
            self.set_speed(speed)

        self.set_frequency(frequency)

        self.set_min(pulses[0], angles[0])
        self.set_max(pulses[1], angles[1])


    def __run__(self, dutycycle, timeout):
        self.action_start()

        self.__write__(dutycycle, timeout)
        self._worker.wait(timeout)

        self.action_stop()


    def __write__(self, dutycycle, timeout):
        self._iface.write(0, dutycycle, timeout)


    def __degrees2time__(self, degrees):
        if degrees != 0:
            return self._speed * abs(degrees)

        else:
            return self._speed * abs(self._angles[1])


    def __degrees2dutycycle__(self, degrees):
        if any(x is None for x in self._angles) and any(x is None for x in self._pulses):
            raise Exception('The "minimum" and "maximum" values of angles and pulses must be defined')

        if degrees < self._angles[0] or degrees > self._angles[1]:
            raise OutRangeError('degrees parameter')

        return self.__pulses2dutycycle__((((self._pulses[1] - self._pulses[0]) / (self._angles[1] - self._angles[0])) * degrees) + self._pulses[0])


    def __pulses2dutycycle__(self, pulse):
        if not all(self._pulses):
            raise Exception('The "minimun" and "maximum" pulses values must be defined')

        return 100 * pulse * self._frequency


    def stop(self):
        """  """

        if self._worker.alive():
            self._iface.stop(0)
            self._worker.stop()


    def alive(self):
        """  """
        return self._worker.alive()


    def set_speed(self, speed):
        """ Allows define the time it takes the servo to move a degrees, this parameter depends on the design/voltage of the servo """

        if not isinstance(speed, (int, long, float)):
            raise InvalidTypeError('The speed for degrees', 'numeric')

        self._speed = speed


    def set_frequency(self, freq):
        """  """

        if not isinstance(freq, (int, long, float)):
            raise InvalidTypeError('The frequency', 'numeric')

        if freq != self._frequency:
            self._frequency = freq
            self._iface.set_frequency(freq)


    def set_min(self, pulse, angle):
        """  """

        if self._worker.alive():
            raise IsRunningError(self.__class__, 'minimum values')

        if not isinstance(pulse, (int, long, float)):
            raise InvalidTypeError('The minimun pulse', 'numeric')

        if not isinstance(angle, (int, long, float)):
            raise InvalidTypeError('The minimun angle', 'numeric')

        if pulse <= 0 or pulse > 1:
            raise OutRangeError('Limit pulse')

        if angle < 0 or angle > 360:
            raise OutRangeError('Limit angle')

        if not self._pulses[1] is None and self._pulses[1] <= pulse:
            raise MinMaxValueError('minimum', 'pulse', 'less', 'maximum')

        if not self._angles[1] is None and self._angles[1] <= angle:
            raise MinMaxValueError('minimum', 'angle', 'less', 'maximum')

        self._pulses[0] = pulse
        self._angles[0] = angle


    def set_max(self, pulse, angle):
        """  """

        if self._worker.alive():
            raise IsRunningError(self.__class__, 'maximum values')

        if not isinstance(pulse, (int, long, float)):
            raise InvalidTypeError('The maximum pulse', 'numeric')

        if not isinstance(angle, (int, long, float)):
            raise InvalidTypeError('The maximum angle', 'numeric')

        if pulse <= 0 or pulse > 1:
            raise OutRangeError('Limit pulse')

        if angle < 0 or angle > 360:
            raise OutRangeError('Limit angle')

        if not self._pulses[0] is None and self._pulses[0] >= pulse:
            raise MinMaxValueError('maximum', 'pulse', 'greater', 'minimum')

        if not self._angles[0] is None and self._angles[0] >= angle:
            raise MinMaxValueError('maximum', 'angle', 'greater', 'minimum')

        self._pulses[1] = pulse
        self._angles[1] = angle


    def backward(self):
        """ Move the servo to minimun angle """
        self._worker.start(args=(self.__pulses2dutycycle__(self._pulses[0]), self.__degrees2time__(self._angles[1])))


    def forward(self):
        """ Move the servo to maximum angle """
        self._worker.start(args=(self.__pulses2dutycycle__(self._pulses[1]), self.__degrees2time__(self._angles[1])))


    def angle_to(self, degrees):
        """ Move the servo to a specific angle """

        if any(x is None for x in self._angles):
            raise Exception('The "minimum" and "maximum" values of angles must be defined')

        if degrees < self._angles[0]:
            raise MinMaxValueError('degrees parameter', 'angle', 'greater', 'minimum')

        if degrees > self._angles[1]:
            raise MinMaxValueError('degrees parameter', 'angle', 'less', 'maximum')

        self._worker.start(args=(self.__degrees2dutycycle__(degrees), self.__degrees2time__(degrees)))
