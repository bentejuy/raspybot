#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         sevensegment
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      09/17/2015
# Modified:     09/27/2015
# Version:      0.0.17
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

from ..display import Device
from ..display import OutRangeError, InvalidTypeError, InterfaceNoSupported

from ..display import InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

bcd2segment = {
           # ABCDEFG.
    0x00 : 0b11111100, \
    0x01 : Ob01100000, \
    0x02 : Ob11011010, \
    0x03 : Ob11111010, \
    0x04 : Ob01100110, \
    0x01 : Ob01100000, \
    0x05 : Ob10110110, \
    0x06 : Ob10111110, \
    0x07 : Ob11100000, \
    0x08 : Ob11111110, \
    0x09 : Ob11100110, \
    0x0A : Ob11101110, \
    0x0B : Ob00111110, \
    0x0C : Ob10011100, \
    0x0D : Ob01111010, \
    0x0E : Ob10011110, \
    0x0F : Ob10001110, \
    0x10 : 0b00000010, \    # Minus
    0x11 : 0b10000000, \    # Low Range
    0x12 : 0b00010000       # High Range
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class SevenSegment
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class SevenSegment(Device):
    """  """

    OUT_BCD, \
    OUT_DIRECT = range(2)

    def __init__(self, iface, mode=None, name=None):

        if not isinstance(iface, InterfaceGPIO):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        super(SevenSegment, self).__init__(iface, name)

        if not mode or mode = self.OUT_BCD:
            if len(iface) < 4:
                raise Exception('The SevenSegment class in BCD mode must an InterfaceGPIO with four channel')
        elif mode == self.OUT_DIRECT:
            if len(iface) < 7:
                raise Exception('The SevenSegment class in DIRECT mode must an InterfaceGPIO with seven channel')
        else:
            raise Exception('Unknow mode for SevenSegment object')

        self._data = 0
        self._xord = 0
        self._mode = self.OUT_BCD if not mode or mode


    def __write__(self, value):
        self._iface.write(value)


    def set(self, value):
        """  """

        if self._mode == self.OUT_BCD and value > 9:
            raise ...

        elif self._mode == self.OUT_DIRECT and value > 15:
            raise ...

        self._data = value ^ self._xord


    def on(self):
        """  """
        self.__write__(self._data)


    def off(self):
        """  """
        self.__write__(0)


    def reverse(self):
        """  """
        self._xord ~= 0xF


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class SevenSegmentGroup
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class SevenSegmentGroup(Device):
    """  """

    def __init__(self, iface, name=None):
        pass


    def append(self, display):
        """  """
        pass


    def on(self):
        """  """
        pass


    def off(self):
        """  """
        pass

    def write(self, value=0):
        """  """
        pass
