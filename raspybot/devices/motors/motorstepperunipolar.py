#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         MotorStepperUnipolar
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/07/2015
# Modified:     07/10/2015
# Version:      0.0.73
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

    For more info see : https://www.youtube.com/watch?v=Dc16mKFA7Fo

"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import logging
import itertools

from ..motor import MotorStepper
from ..motor import InvalidTypeError, UnknowMotorModeError, IsRunningError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class MotorStepperUnipolar
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class MotorStepperUnipolar(MotorStepper):
    MODE_SINGLE, \
    MODE_DUAL, \
    MODE_HALF = range(3)

    def __init__(self, iface, name=None, mode=None, start=None, stop=None):
        super(MotorStepperUnipolar, self).__init__(iface, name, start, stop)

        self._mode = 0
        self._steps = (0b0001, 0b0011, 0b0010, 0b0110, 0b0100, 0b1100, 0b1000, 0b1001)

        self.set_mode(mode or self.MODE_SINGLE)


    def __next__(self):
        if self._mode == self.MODE_HALF:
            limit = 7
            index = range(0, 8)

        elif self._mode == self.MODE_SINGLE:
            limit = 6
            index = range(0, 7, 2)

        else:
            limit = 7
            index = range(1, 8, 2)

        iterator = itertools.cycle(index)

        if self._index < limit:
            while self._index > next(iterator):
                pass

        return iterator


        """
        if self._mode == self.MODE_SINGLE:
            # Steps in this mode 0, 2, 4, 6
            if self._state >= 6:
                self._state = 0
            else:
                self._state += 2 - self._state % 2

        elif self._mode == self.MODE_DUAL:
            # Steps in this mode 1, 3, 5, 7
            if self._state >= 7:
                self._state = 1
            else:
                self._state += 1 + self._state % 2
        else:
            # All Steps
            if self._state >= 7:
                self._state = 0
            else:
                self._state += 1

        return self._state
        """

    def __prev__(self):
        if self._mode == self.MODE_HALF:
            limit = 0
            index = range(7, -1, -1)

        elif self._mode == self.MODE_SINGLE:
            limit = 0
            index = range(6, -1, -2)

        else:
            limit = 1
            index = range(7, 0, -2)

        iterator = itertools.cycle(index)

        if self._index > limit:
            while self._index < next(iterator):
                pass

        return iterator


        """
        if self._mode == self.MODE_SINGLE:
            # Steps in this mode 0, 2, 4, 6
            if self._state <= 0:
                self._state = 6
            else:
                self._state -= 2 - self._state % 2

        elif self._mode == self.MODE_DUAL:
            # Steps in this mode 1, 3, 5, 7
            if self._state <= 1:
                self._state = 7
            else:
                self._state -= 1 + self._state % 2
        else:
            # All Steps
            if self._state <= 0:
                self._state = 7
            else:
                self._state -= 1

        return self._state
        """

    def __time2steps__(self, time):
        if not isinstance(time, (int, long, float)):
            raise InvalidTypeError('Time', 'numeric')

        if time >= 0:
            return int(time / float(self._delay))

        else:
            return 0


    def __angle2steps__(self, angle):
        if not isinstance(angle, (int, long, float)):
            raise InvalidTypeError('Angle', 'numeric')

        if not self._degrees:
            raise ValueError('Not was defined the value of manufactures angle per step')

        if self._mode == self.MODE_HALF:
            return int(angle / self._degrees)
        else:
            return int(angle / (self._degrees * 2))


    def set_mode(self, mode):
        """ """

        if not isinstance(mode, (int, long)):
            raise InvalidTypeError('Mode' , 'motor mode')

        if mode < self.MODE_SINGLE or mode > self.MODE_HALF:
            raise UnknowMotorModeError()

        if self._worker.alive():
            raise IsRunningError(self.__class__, 'mode')

        self._mode = mode
