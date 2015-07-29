#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         MotorServo
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/27/2015
# Modified:     07/08/2015
# Version:      0.0.23
# Copyright:    (c) 2015 Bentejuy Lopez
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

    Important: This module has not been tested, it may contain multiple errors

    For more info see : https://www.youtube.com/watch?v=ddlDgUymbxc

"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import logging

from ..motor import Worker, MotorBase
from ..motor import InvalidTypeError, OutRangeError, IsRunningError, InvalidRangeError, MinMaxValueError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class MotorServo
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class MotorServo(MotorBase):
    def __init__(self, iface, pulses, angles, speed=None, frec=None, name=None, start=None, stop=None):
        super(MotorServo, self).__init__(iface, name, start, stop)

        self._delay  = 0.02
        self._state  = 0
        self._speed  = 0.01
        self._pulses = [None, None]
        self._angles = [None, None]
        self._timeout = 0.0005

        self._worker =  Worker(self.__run__)

        if not isinstance(pulses, (tuple, list)) or len(pulses) <> 2:
            raise InvalidRangeError('pulses')

        if not isinstance(angles, (tuple, list)) or len(angles) <> 2:
            raise InvalidRangeError('angles')

        if speed:
            self.set_speed(speed)

        self.set_min(pulses[0], angles[0])
        self.set_max(pulses[1], angles[1])


    def __run__(self, count):
        self.action_start()

        while not self._worker.is_set():
            try:
                count -= 1
                self.__write__(1)

                if count <= 0:
                    self._worker.set()

                self._worker.wait(self._delay)

            except Exception, error:
                logger.critical(error)

        self.action_stop()


    def __write__(self, value):
        self._iface.write(value, self._timeout)


    def __degrees2cicles__(self, degrees):
        if degrees >= 0:
            return self._speed * degrees / self._delay
        else:
            return 0

    def __degrees2pulses__(self, degrees):
        if not all(self._pulses) or not all(self._angles):
            raise Exception('The "min" and "max" angle and pulse values must be defined')

        if degrees > min(self._degrees) or degrees < max(self._degrees):
            raise OutRangeError('degrees parameter')

        return float((((self._pulses[1] - self._pulses[0]) / (self._angles[1] - self._angles[0])) * degrees + self._pulses[0])/2)


    def stop(self):
        if self._worker.alive():
            self._worker.__stop__()

        self.__write__(0)


    def alive(self):
        return self._worker.alive()


    def set_frequency(self, herz):
        ''' ... '''
        if not isinstance(herz, (int, long, float)):
            raise InvalidTypeError('The frequency', 'numeric')

        self._delay = 1 / herz


    def set_speed(self, speed):
        """ Allow define the time it takes the servo to move a degree, this parameter depends on the design of the servo """

        if not isinstance(speed, (int, long, float)):
            raise InvalidTypeError('The speed for degrees', 'numeric')

        self._speed = speed


    def set_min(self, pulse, angle):
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
            raise MinMaxValueError('min', 'pulse', 'less', 'maximum')

        if not self._angles[1] is None and self._angles[1] <= angle:
            raise MinMaxValueError('min', 'angle', 'less', 'maximum')

        self._pulses[0] = pulse
        self._angles[0] = angle


    def set_max(self, pulse, angle):
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
            raise MinMaxValueError('max', 'pulse', 'greater' 'minimum')

        if not self._angles[0] is None and self._angles[0] >= angle:
            raise MinMaxValueError('max', 'angle', 'greater' 'minimum')

        self._pulses[1] = pulse
        self._angles[1] = angle


    def backward(self):
        self._state = self._pulses[0]
        self._timeout = self._pulses[1]

        self._worker.__start__(args=(self.__degrees2cicles__(180),))
#       self._worker.__start__(args=(self.__degrees2cicles__(self._angles[0]),))


    def forward(self):
#       self._delay = self._pulses[1]
        self._state = self._pulses[1]
        self._timeout = self._pulses[0]

        self._worker.__start__(args=(self.__degrees2cicles__(180),))
#       self._worker.__start__(args=(self.__degrees2cicles__(self._angles[1]),))


    def goto(self, degrees):
#       self._delay = self.__degrees2pulses__(degrees)
        self._state = self._delay
        self._timeout = self._delay / 2

        self._worker.__start__(args=(self.__degrees2cicles__(degrees),))


    def angle_to(self, degrees):
        pass
