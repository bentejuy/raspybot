#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         lcd2004a
# Purpose:      Specific object to control LCD 1602A
#
# Author:       Bentejuy Lopez
# Created:      01/08/2016
# Modified:     01/10/2016
# Version:      0.0.13
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
# Class LCD1602AD
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class LCD2004A(HD44780):

    def __init__(self, iface):

        self._rows = 4
        self._cols = 20
        self._offsets = (0x00, 0x40, 0x14, 0x54)

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

        super(LCD2004A, self).__init__(iface)
