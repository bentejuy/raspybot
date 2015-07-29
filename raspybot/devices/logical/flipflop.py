#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         flipflop
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      03/13/2015
# Modified:     07/08/2015
# Version:      0.0.33
# Copyright:    (c) 2015 Bentejuy Lopez
# Licence:      GPLv3
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

from ..logic import Device
from ..logic import OutRangeError,InvalidFunctionError, InvalidTypeError, InterfaceNoSupported

from ..logic import InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class FlipFlop
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class FlipFlop(Device):
    """ Store the value of one or more states for work with him and simulate a FlipFlop electronic element. """

    def __init__(self, iface, name=None, initial=0):

        if not isinstance(iface, InterfaceGPIO):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        super(FlipFlop, self).__init__(iface, name)

        if len(iface) < 0 or len(iface) > 8:
            raise OutRangeError('The length of interface ports')

        self._iface  = iface
        self._value  = initial
        self._sizeof = len(self._iface.get_out_ports())   # Cuando no sea una interfaceGPIO habra que ver como determino el tamaño en bits....

        self.__write__(initial)


    def __write__(self, value):
        self._iface.write(value)


    def __index2bin__(self, index):
        if isinstance(index, (int, long)):
            raise InvalidTypeError('"index" value', 'integer or long', 'number')

        if index >= self._sizeof:
            raise Exception('The value of the pin position is too large')

        return 1 << index


    def get(self):
        """ Return the value of internal state of channels as integer. """

        return self._value


    def set(self, index=None):
        """ Set one channel, a tuple or list of channel to 1 logical.

           Arg:
              index: An integer, tuple or list of integers where the the integer is the index
                     position into channel, starting of zero. If "index" is not defined then all
                     channel are set to 1.
           Return:
              Nothing.
        """

        if index is not None:
            if isinstance(index, (tuple, list)):
                for i in index:
                    self._value |= self.__index2bin__(i)

            else:
                self._value |= self.__index2bin__(index)

        else:
            self._value = 2 ** self._sizeof - 1

        self.__write__(self._value)


    def reset(self, index=None):
        """ Set one channel, a tuple or list of channel to 0 logical.

           Arg:
              index: An integer, tuple or list of integers where the the integer is the index
                     position into channel, starting of zero. If "index" is not defined then all
                     channel are set to 0.
           Return:
              Nothing.
        """

        if index is not None:
            if isinstance(index, (tuple, list)):
                for i in index:
                    self._value &= ~ self.__index2bin__(i)

            else:
                self._value &= ~ self.__index2bin__(index)

        else:
            self._value = 0

        self.__write__(self._value)


    def toggle(self):
        """ Invert the value of all channels. """

        self._value = ~ self._value
        self.__write__(self._value)
