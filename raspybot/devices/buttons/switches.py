#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         switches
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      04/01/2015
# Modified:     01/31/2016
# Version:      0.0.25
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

from ..button import gpio
from ..button import Buttons

from ..button import InvalidFunctionError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class Switches
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class Switches(Buttons):
    """ Controls the state of one or more inputs channels """

    OFF, \
    ON = range(2)

    def __init__(self, iface, change, name=None):
        super(Switches, self).__init__(iface, name, clicked=self.__on_change__, release=self.__on_change__)

        if not hasattr(change, '__call__'):
            raise InvalidFunctionError('change')

        self._on_change = change


    def __on_change__(self, obj, pin, mode):
        self._on_change(self, pin, self.ON if self.CLICKED else self.OFF)


    def setup(self, pin, pud=gpio.PUD_DOWN, bouncetime=200):
        """ Sets the configuration for channel previously declared in the interface.

            Args:
                pin: The number channel.
                pud: The value of initial PUD, can be gpio.PUD_UP or gpio.PUD_DOWN. By default is gpio.PUD_DOWN.
                bouncetime: Time in milliseconds to ignoring further edges for switch bounce handling.
        """
        super(self.__class__, self).setup(pin, self.CLICKED, pud, bouncetime)
        super(self.__class__, self).setup(pin, self.RELEASE, pud, bouncetime)

