#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         interfacepwm
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      07/22/2015
# Modified:     07/30/2015
# Version:      0.0.25
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

import logging

from ..interface import TaskPWM
from ..interface import InterfaceActive

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class InterfacePWM
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class InterfacePWM(InterfaceActive):
    """

    """

    def __init__(self, manager, pinout=None, frequency=50):
        super(InterfacePWM, self).__init__(manager, self.__parser__)

        self._pin = None
        self._pwm = None
        self._bus = manager.get_connection(self)
        self._frequency = 50

        if pinout:
            self.setup(pinout, frequency)

        self._manager.append(self)


    def __len__(self):
        return 1
#       return len(self._pinout)


    def __parser__(self, task):
        state = task.get_state()

        if state == task.WAITING:
            if task.action == task.PWM_START:
                if state == task.WAITING:
                    self._pwm.start(task.dutycycle)

            elif task.action == task.PWM_STOP:
                self._pwm.stop()
                del self._pwm
                self._pwm = None

        elif state == task.TIMEOUT or state == task.STOPPED:
            self._pwm.stop()
            del self._pwm
            self._pwm = None

        return 0


    def __contains__(self, pin):
        return pin == self._pin


    def setup(self, pin, frequency=50):
        """  """

        if self._pwm:
            self._manager.cleanup(self._pin)
            self._pin = None
            del self._pwm

        self._manager.setup(pin, self._bus.HARD_PWM)
        self._frequency = frequency
        self._pin = pin
        self._pwm = self._bus.PWM(pin, self._frequency)


    def stop(self):
        """  """

        super(self.__class__, self).__stop__()
        super(self.__class__, self).__append__(TaskPWM(TaskPWM.PWM_STOP))

        if not self.alive():
            super(self.__class__, self).__start__()


    def write(self, dutycycle, timeout=-1):
        """ """

        if not self._pwm:
            self._pwm = self._bus.PWM(self._pin, self._frequency)

        super(self.__class__, self).__append__(TaskPWM(TaskPWM.PWM_START, dutycycle, timeout))

        if not self.alive():
            super(self.__class__, self).__start__()


    def set_frequency(self, freq):
        """  """

        self._frequency = freq

