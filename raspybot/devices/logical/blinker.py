#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         blinker
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      03/13/2015
# Modified:     07/08/2015
# Version:      0.0.49
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time
import logging

from ..logic import Worker
from ..logic import ActionDevice
from ..logic import OutRangeError, InvalidFunctionError, InvalidTypeError, IsRunningError

from ..logic import InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class Blinker
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class Blinker(ActionDevice):
    """ Send intermittent pulses, being able to vary the speed and the value we want to send. """

    def __init__(self, iface, name=None, delay=1, initial=0, checker=None, start=None, stop=None):

        if not isinstance(iface, InterfaceGPIO):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        super(Blinker, self).__init__(iface, name, start, stop)

        self._delay = 1
        self._value = 0
        self._counter = 0
        self._checker = None
        self._worker = Worker(self.__run__)

        self.set_delay(delay)
        self.set_value(initial)
        self.set_callback(checker)


    def __write__(self, value):
        self._iface.write(value)


    def __run__(self, timelive=None):
        self.action_start()

        if timelive:
            timelive += time.time()

        self._counter = 0

        while not self._worker.is_set():
            try:
                self.__write__(self._value)

                if not self._checker:
                    self._value = ~self._value & 0xFF
                else:
                    try:
                        self._value = self._checker(self._value, self._counter)
                        self._counter += 1

                    except:
                        self.stop()

                self._worker.wait(self._delay)

                if timelive and timelive <= time.time():
                    self.stop()

            except Exception, error:
                logger.critical(error)

        self.action_stop()


    def start(self, timelive=None):
        """  """

        if isinstance(timelive, (int, long, float)):
            if timelive < self._delay:
                raise ValueError('The "timelive" parameter must be greater that the delay time')

        self._worker.__start__((timelive,))


    def stop(self):
        """  """

        if self._worker.alive():
            self._worker.__stop__()

        self.__write__(0)


    def join(self):
        """  """

        self._worker.join()


    def alive(self):
        """  """

        return self._worker.alive()


    def set_delay(self, delay):
        """  """

        if not isinstance(delay, (int, long, float)):
            raise InvalidTypeError('The delay', 'numeric')

        if self._worker.alive():
            raise IsRunningError(self.__class__, 'delay')

        self._delay = delay


    def set_value(self, value):
        """  """

        if not isinstance(value, (int, long, float)):
            raise InvalidTypeError('The delay', 'numeric')

        if self._worker.alive():
            raise IsRunningError(self.__class__, 'delay')

        if value < 0x00 and value > 0xFF:
            raise OutRangeError('The initial value')

        self._value = value


    def set_callback(self, callback):
        """  """

        if callback and not hasattr(callback, '__call__'):
            raise InvalidFunctionError('checker')

        working = self.alive()

        if working:
            self.stop()

        self._checker = callback

        if working:
            self.start()


    def set(self, delay, initial, checker):
        """  """

        self.set_delay(delay)
        self.set_value(initial)
        self.set_callback(checker)