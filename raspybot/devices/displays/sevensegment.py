#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         sevensegment
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      09/17/2015
# Modified:     12/15/2015
# Version:      0.0.59
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

from math import log

from ..display import Worker
from ..display import Device
from ..display import OutRangeError, InvalidTypeError, InterfaceNoSupported

from ..display import InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


NUM2SEGMENTS = {
           #.GFEDCBA
    0x00: 0b00111111, \
    0x01: 0b00000110, \
    0x02: 0b01011011, \
    0x03: 0b01001111, \
    0x04: 0b01100110, \
    0x05: 0b01101101, \
    0x06: 0b01111101, \
    0x07: 0b00000111, \
    0x08: 0b01111111, \
    0x09: 0b01100111, \
    0x0A: 0b01110111, \
    0x0B: 0b01111100, \
    0x0C: 0b00111001, \
    0x0D: 0b01011110, \
    0x0E: 0b01111001, \
    0x0F: 0b01110001, \
    0x10: 0b01000000, \
    0x11: 0b10000000, \
    0x12: 0b00010000
}

'''
    0x00 -> 0
    0x01 -> 1
    0x02 -> 2
    0x03 -> 3
    0x04 -> 4
    0x05 -> 5
    0x06 -> 6
    0x07 -> 7
    0x08 -> 8
    0x09 -> 9
    0x0A -> A
    0x0B -> b
    0x0C -> C
    0x0D -> d
    0x0E -> E
    0x0F -> F
    0x10 -> Minus
    0x11 -> Low Range
    0x12 -> High Range
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class SevenSegment
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class SevenSegment(Device):
    """  """

    BCD_MODE, \
    DIRECT_MODE = range(2)

    def __init__(self, iface, mode=None, name=None):

        if not isinstance(iface, InterfaceGPIO):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        super(SevenSegment, self).__init__(iface, name)

        if not mode or mode == self.BCD_MODE:
            if len(iface) < 4:
                raise Exception('The SevenSegment object in BCD mode must an InterfaceGPIO with four channel')

        elif mode == self.DIRECT_MODE:
            if len(iface) < 7:
                raise Exception('The SevenSegment object in DIRECT mode must an InterfaceGPIO with seven channel')

        else:
            raise Exception('Unknow mode for SevenSegment object')

        self._data = 0
        self._xord = 0xFF
        self._mode = self.BCD_MODE if not mode else mode

        self.off()


    def __value2segment__(self, value):
        if self._mode == self.BCD_MODE:
            return value
        elif self._mode == self.DIRECT_MODE:
            return NUM2SEGMENTS[value]

        return 0


    def __write__(self, value):
        self._iface.write(value)


    def set(self, value, on=True):
        """ Set the value to the seven segment display, optatively turn on with the new value  """

        if self._mode == self.BCD_MODE:
            if value > 9:
                raise OutRangeError(value, 'in BCD mode')

            self._data = value ^ self._xord

        elif self._mode == self.DIRECT_MODE:
            if value > 15:
                raise OutRangeError(value, 'in Direct mode')

            self._data = NUM2SEGMENTS[value]

        if on:
            self.__write__(self._data ^ self._xord)


    def on(self):
        """ Turns on the segments with the value stored """
        self.__write__(self._data)


    def off(self):
        """ Turns off all segment """
        self.__write__(0 ^ self._xord)


    def inverted(self):
        """ Inverts the output to control seven segment displays with common anode or cathode. """
        self._xord ^= 0xFF


    def dot(self, state):
        """  Turn on or off the dot on the seven segment display. """

        if self._mode == self.BCD_MODE:
            self.__write__((self._data | (0x10 if state else 0x00)) ^ self._xord)
        else:
            self.__write__((self._data | (0x80 if state else 0x00)) ^ self._xord)


    def get_mode(self):
        """ Returns the work mode defined on creation time """
        return self._mode


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class SevenSegments
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class SevenSegments(Device):
    """  """

    def __init__(self, iface, name=None):

        if not isinstance(iface, InterfaceGPIO):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        super(SevenSegments, self).__init__(iface, name)

        self._xord = 0xFF
        self._value = 0
        self._displays = []

        self._worker =  Worker(self.__run__)


    def __run__(self):
        value = self._value
        delay = 1 / (30.0 * len(self._displays))        # Trying to maintain a higher refresh time to 25 times per second

        for display in self._displays:
            display.off()

            if value:
                display.set(value % 10, False)
                value /= 10

        index = 0
        value = (2 ** len(self._displays)) >> 1

        while not worker.is_set():
            if not index:
                index = value
            else:
                index >>= 1

            self._displays[int(log(index, 2))].on()

            self._iface.write(index ^ self.xord)
            self._worker.wait(delay)

            index >>= 1


    def inverted(self):
        """ Inverts the output to control seven segment displays with common anode or cathode. """
        self._xord ^= 0xFF


    def append(self, display):
        """ Append new SevenSegment object """

        if not isinstance(display, SevenSegment):
            raise Exception('The display parameter must be a valid SevenSegment object')

        if len(self._iface) < len(self._displays):
            raise Exception('La Interfaz definida no puede soportar mas display de siete Segmentos')

        if any([display.get_mode() != x.get_mode() for x in self._display]):
            raise Exception('Todas los display necesitan trabajar en el mismo modo')

        self._display.append(display)


    def on(self):
        """ Turns on all SevenSegment displays  """

        if not self._worker.alive():
            self._worker.__start__()


    def off(self):
        """ Turns off all SevenSegment displays """

        if self._worker.alive():
            self._worker.__stop__()


    def write(self, value=0):
        """ Writes a numeric value in the SevenSegment displays """

        if not isinstance(value, (int, long)):
            raise InvalidTypeError('Value', 'numeric')

        if abs(value) > (10 ** len(self._display) - 1):
            raise OverflowError('Value is out of range')


        if self._worker.alive():
            self._worker.__stop__()

        self._value = abs(value)
        self._worker.__start__()

