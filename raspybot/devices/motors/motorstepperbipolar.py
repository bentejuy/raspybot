#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         MotorStepperBipolar
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      07/01/2015
# Modified:     27/03/2015
# Version:      0.0.67
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
from ..motor import InvalidTypeError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class MotorStepperBipolar
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class MotorStepperBipolar(MotorStepper):
    def __init__(self, iface, name=None, start=None, stop=None):
        super(MotorStepperBipolar, self).__init__(iface, name, start, stop)

        self._steps = (0b0101, 0b0110, 0b1010, 0b1001)


    def __next__(self):
        iterator = itertools.cycle(range(4))

        if self._index < 3:
            while self._index > next(iterator):
                pass

        return iterator

        """
        if self._state >= 3:
            self._state = 0
        else:
            self._state += 1

        return self._state
        """


    def __prev__(self):
        iterator = itertools.cycle(range(3, -1, -1))

        if self._index > 0:
            while self._index < next(iterator):
                pass

        return iterator

        """
        if self._state <= 0:
            self._state = 3
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
            raise ValueError('Not defined the value of manufactures the angle per step')

        return int(angle / self._degrees)
