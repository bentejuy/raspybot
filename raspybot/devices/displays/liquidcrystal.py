#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         liquidcrystal
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      11/29/2015
# Modified:     02/08/2016
# Version:      0.0.63
# Copyright:    (c) 2015-2016 Bentejuy Lopez
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

from ..display import InterfaceNoSupported, InvalidInterfaceError, InterfaceSizeMustBe

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

    LCD1602A, \
    LCD2004A = range(2)

    def __init__(self, iface, model, name=None):
        super(LiquidCrystal, self).__init__(iface, name)

        try:
            if model == self.LCD1602A:
                from parts.lcd1602a import LCD1602A as lcd

            elif model == self.LCD2004A:
                from parts.lcd2004a import LCD2004A as lcd

        except ImportError as error:
           raise ImportError("Can't load the {0} LCD model module: {1}".format('', error))  # Corregir y extraer nombre de la exception

        except:
            raise

        self._part = lcd(iface)

        for mth in [mth for mth in dir(self._part) if not mth.startswith('__') and hasattr(getattr(self._part, mth), '__call__')]:
            if not hasattr(self, mth):
                setattr(self, mth, getattr(self._part, mth))


    def on(self):
        """  """
        self._part.on()


    def off(self):
        """  """
        self._part.off()


    def clear(self):
        """  """
        self._part.clear()


    def home(self):
        """  """
        self._part.home()


    def goto(self, col, row):
        """  """
        self._part.goto(col, row)


    def blinker(self, on=None):
        """  """
        self._part.blinker(on)


    def write(self, char, col=None, row=None):
        """  """
        self._part.write(char, col, row)


    def writeln(self, text, line=None):
        """ """
        self._part.writeln(text, line)


    def set_cursor(self, enable, blink=True):
        """  """
        self._part.set_cursor(enable, blink)

