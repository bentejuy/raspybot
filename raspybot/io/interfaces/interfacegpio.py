#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         interfacegpio
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/07/2015
# Modified:     01/03/2015
# Version:      0.0.83
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

from ..interface import TaskGPIO
from ..interface import InterfaceActive
from ..interface import InvalidTypeError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class InterfaceGPIO
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class InterfaceGPIO(InterfaceActive):
    """
        Interface to interact directly with the GPIO ports, it can receive four parameters.

        manager: The manager interfaces
        pinin  : An integer, tuple or list of integers used as data inputs.
        pinout : An integer, tuple or list of integers used as data output.
        callback: Function that will be called when data is received at the input channels (pinint)
    """

    def __init__(self, manager, pinin=None, pinout=None, callback=None):
        super(InterfaceGPIO, self).__init__(manager, self.__parser__)

        self._pinin  = []
        self._pinout = []

        self._bus = manager.get_connection(self)

        if pinout:
            self.setup(pinout, self._bus.OUT)

        if pinin:
            self.setup(pinin, self._bus.IN, callback)

        self._manager.append(self)


    def __len__(self):
        return len(self._pinin) + len(self._pinout)


    def __write__(self, data):
        try:
            for pin in self._pinout:
                self._bus.output(pin, data & 0x1)
                data = data >> 1

        except Exception as error:
            logger.error(error)


    def __parser__(self, task):
        state = task.get_state()

        if task.action == task.GPIO_WRITE:
            if state == task.WAITING:
                self.__write__(task.data)

                return task.set_state(task.RUNNING)

            if state == task.CONSTANT:
                self.__write__(task.data)

                return 0

            if state >= task.STOPPED:
                self.__write__(0)

                return 0

            if state == task.RUNNING:
                return 0

        else:
            pass

        return 0


    def __contains__(self, pin):
        return pin in self._pinin or pin in self._pinout


    def free(self):
        """ Frees all input and output channels. """

        self.clear()
        map(self._manager.cleanup, self._pinin)
        map(self._manager.cleanup, self._pinout)

        self._pinin = []
        self._pinout = []


    def setup(self, pin, mode, initial=0, callback=None, pud=None, edge=None, bouncetime=200):
        """ Sets the parameters of one or more channels as input or output. """

        def append_in(pin, mode):
            if mode == self._bus.IN:
                if pin in self._pinout:
                    self._pinout.remove(pin)
                if pin not in self._pinin:
                    self._pinin.append(pin)

            else:
                if pin in self._pinin:
                    self._pinin.remove(p)
                if pin not in self._pinout:
                    self._pinout.append(pin)

        if mode == self._bus.IN:
            pud = self._bus.PUD_DOWN if pud is None else pud
            edge = self._bus.BOTH if edge is None else edge

        if isinstance(pin, (tuple, list)):
            for p in pin:
                self._manager.setup(p, mode, initial, callback, pud, edge, bouncetime, self)
                append_in(p, mode)

        else:
            self._manager.setup(pin, mode, initial, callback, pud, edge, bouncetime, self)
            append_in(pin, mode)


    def clear(self):
        """ Empty the tasks from queue read and write. """
        super(self.__class__, self).__stop__()


    def stop(self):
        """ Stops all pending writes and sets all channel to zero. """

        super(self.__class__, self).__stop__()
        super(self.__class__, self).__append__(TaskGPIO(TaskGPIO.GPIO_STOP))

        if not self.alive():
            super(self.__class__, self).__start__()


    def write(self, data, timeout=-1):
        """ Adds a binary value to the queue to write in the output channels. """

        super(self.__class__, self).__append__(TaskGPIO(TaskGPIO.GPIO_WRITE, data, timeout))

        if not self.alive():
            super(self.__class__, self).__start__()


    def quickly(self, data):
        """ Writes directly to the output channels without delay, only if it does not have any queued task. """

        if not self.alive():
            self.__write__(data)


    def get_input_channels(self):
        """ Returns all input channels used by this Interface. """
        return self._pinin


    def get_output_channels(self):
        """ Returns all output channels used by this Interface. """
        return self._pinout
