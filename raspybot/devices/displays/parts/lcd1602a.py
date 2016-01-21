#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         lcd1602a
# Purpose:      Specific object to control LCD 1602A
#
# Author:       Bentejuy Lopez
# Created:      01/08/2016
# Modified:     01/10/2016
# Version:      0.0.23
# Copyright:
# Licence:      GLPv3
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from .hd44780 import HD44780

from ..liquidcrystal import InterfaceGPIO, InterfaceI2CSlave
from ..liquidcrystal import InvalidInterfaceError, InterfaceSizeMustBe

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class LCD1602A
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class LCD1602A(HD44780):
    """
        The LCD1602 allow two interfaces types, direct connection with gpio
        channels and I2C protocols.

        In direct connection, it can work with an Interface of 7 or 11 channels,
        the distribution of channels must be in this order (depending of numbers
        of channels):

            RS, RW, EN, D4-D7 or RS, RW, EN, D0-D7,

        With the mode I2C, its assumed that the low byte are the control bits
        (RS, RW, EN and BackLight) and the high bits are the data (D4 to D7). 
        This bit distribution is intended for the PCF8574 integrated circuit or
        equivalents.

    """


    def __init__(self, iface):

        self._rows = 2
        self._cols = 16
        self._offsets = (0x00, 0x40)

        if isinstance(iface, InterfaceGPIO):
            if not len(iface) in (7, 11):
                raise InterfaceSizeMustBe(iface.__class__, 6)

            self._double = len(iface) >= 11
            self.__write__ = self.__write_gpio__

        elif isinstance(iface, InterfaceI2CSlave):
            self._double = False
            self.__write__ = self.__write_i2c__

        else:
            raise InvalidInterfaceError

        super(LCD1602A, self).__init__(iface)

