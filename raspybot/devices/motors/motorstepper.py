#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         MotorStepper
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/07/2015
# Modified:     12/29/2015
# Version:      0.0.87
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

from ..motor import Worker
from ..motor import MotorBase
from ..motor import InvalidTypeError, IsRunningError, MinMaxValueError, InterfaceNoSupported

from ..motor import InterfaceGPIO
from ..motor import InterfaceI2CSlave

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class MotorStepperUnipolar
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class MotorStepper(MotorBase):
    def __init__(self, iface, name, start, stop):

        if not isinstance(iface, (InterfaceGPIO, InterfaceI2CSlave)):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        super(MotorStepper, self).__init__(iface, name, start, stop)

        self._index = -1                                    # Last position in the tuple of steps
        self._steps = None                                  # Tuple with all possible steps
        self._delay = 0.001                                 # Delay until next step
        self._factor = 0.0005                               # Correction factor, because "delay" is the sleeping time, it does not count the time it takes to process the remaining instructions ....
        self._degrees = None                                # Degrees that the stepper motor moves per each step taken

        self._worker =  Worker(self.__run__)


    def __next__(self):
        pass


    def __prev__(self):
        pass


    def __run__(self, steps, moveto):
        self.action_start()

        delay = self._delay - self._factor

        if moveto == self.MOVE_LEFT:
            for self._index in self.__prev__():
                self.__write__(self._steps[self._index])

                if steps > 0:
                    steps -= 1

                elif steps == 0:
                    break

                if self._worker.is_set():
                    break

                self._worker.wait(delay)

        else:
            for self._index in self.__next__():
                self.__write__(self._steps[self._index])

                if steps > 0:
                    steps -= 1

                elif steps == 0:
                    break;

                if self._worker.is_set():
                    break

                self._worker.wait(delay)

        self._worker.wait(delay)
        self.__write__(0)

        self.action_stop()


    def __write__(self, value):
        self._iface.write(value)


    def __angle2steps__(self, angle):
        pass


    def stop(self):
        """  """

        if self._worker.alive():
            self.__write__(0)
            self._worker.__stop__()


    def join(self):
        """  """
        self._worker.join()


    def alive(self):
        """  """
        return self._worker.alive()


    def set_factor(self, factor):
        """  """

        if self._worker.alive():
            raise IsRunningError(self.__class__, ' Correction factor')

        if not isinstance(factor, (int, float)):
            raise InvalidTypeError('The Factor correction', 'numeric', 'defined in seconds')

        if factor >= self._delay:
            raise MinMaxValueError('Correction Factor', '', 'less', 'delay')

        self._factor = factor


    def set_speed(self, rpm):
        """  """

        if self._worker.alive():
            raise IsRunningError(self.__class__, 'speed')

        if not isinstance(rpm, (int, long)):
            raise InvalidTypeError('The Speed', 'numeric', 'defined in RPM')

        self._delay = 60 / float(self.__angle2steps__(360) * rpm)


    def set_degrees(self, degrees):
        """  """

        if self._worker.alive():
            raise IsRunningError(self.__class__, 'degrees per step')

        if not isinstance(degrees, (int, long, float)):
            raise InvalidTypeError('The degrees per step', 'numeric')

        if degrees < 0.01 or degrees > 15:
            raise OutRangeError('Limit degrees', ', set degrees per step')

        self._degrees = degrees


    def backward(self, steps=-1, degrees=0):
        """ Move the motor to the left, the parameters are mutually exclusive, only accepts one on each call.
            Without parameters the motor will move indefinitely in the opposite direction of clockwise. """

        if degrees:
            steps = self.__angle2steps__(degrees)

        self._worker.__start__(args=(steps, self.MOVE_LEFT))


    def forward(self, steps=-1, degrees=0):
        """ Move the motor to the right, the parameters are mutually exclusive, only accepts one on each call.
            Without parameters the motor will move indefinitely in the opposite direction of clockwise. """

        if degrees:
            steps = self.__angle2steps__(degrees)

        self._worker.__start__(args=(steps, self.MOVE_RIGHT))


    def angle_to(self, degrees):
        """ This function moves the motor a certain number of degrees. To function properly, previously you need
            set the ratio of degrees per steps determined by the manufacturer. """

        if degrees > 0:
            self.forward(degrees=degrees)
        elif degrees < 0:
            self.backward(degrees=degrees * -1)
