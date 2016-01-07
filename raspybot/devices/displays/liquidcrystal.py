#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         liquidcrystal
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      11/29/2015
# Modified:     01/03/2016
# Version:      0.0.33
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

from ..display import Device

from ..display import InterfaceGPIO
from ..display import InterfaceI2CSlave

from ..display import InterfaceNoSupported, InterfaceTypeMustBe, InterfaceSizeMustBe

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class LiquidCristal
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class LiquidCrystal(Device):
    """

    """

    LCD1602A_I2C, \
    LCD1602A_GPIO = range(2)


    def __init__(self, iface, model, name=None):

        if model == self.LCD1602A_GPIO:
            if not isinstance(iface, InterfaceGPIO):
                raise InterfaceTypeMustBe(self.__class__, iface.__class__)

            if not len(iface) in (6, 10):
                raise InterfaceSizeMustBe(iface.__class__, 6)

            try:
                from parts.lcd1602a import LCD1602AD as lcd

            except ImportError as error:
               raise ImportError("Can't load the {0} LCD model module: {1}".format('', error))

        elif model == self.LCD1602A_I2C:
            raise NotImplementedError


        part = lcd(iface)

        for mth in [mth for mth in dir(part) if not mth.startswith('__') and hasattr(getattr(part, mth), '__call__')]:
            setattr(self, mth, getattr(part, mth))


    def on(self):
        """  """
        raise NotImplementedError


    def off(self):
        """  """
        raise NotImplementedError


    def clear(self):
        """  """
        raise NotImplementedError


    def home(self):
        """  """
        raise NotImplementedError


    def goto(self, x, y):
        """  """
        raise NotImplementedError


    def blinker(self, on=None):
        """  """
        raise NotImplementedError


    def write(self, char, x, y):
        """  """
        raise NotImplementedError


    def writeln(self, text):
        """ """
        raise NotImplementedError


    def set_cursor(self, enable, blink=True):
        """  """
        raise NotImplementedError


