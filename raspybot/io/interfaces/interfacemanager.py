#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         interfacemanager
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/07/2015
# Modified:     07/28/2015
# Version:      0.0.73
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
import exceptions

from ..interface import gpio
from ..interface import InterfaceGPIO
from ..interface import ExceptionFmt, InvalidInterfaceError, InvalidTypeError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Internal Exceptions
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class UnknowTypeChannelError(Exception):
    def __str__(self):
        return 'Unknown mode type port'


class InUseChannelError(ExceptionFmt):
    def __init__(self, value):
        super(InUseChannelError, self).__init__('The channel {0} is in use by interface class {1}({2})', channel, iface, name)


class InvalidModeChannelError(ExceptionFmt):
    def __init__(self, value):
        super(InvalidModeChannelError, self).__init__('Configuring channel "{0}" in an invalid mode.', channel)


class NotFoundInterfaceError(Exception):
    def __str__(self):
        return 'Interface not found'


class InvalidInterfaceError(Exception):
    def __str__(self):
        return 'The interface must be a valid "Interface" object'


class DuplicateInterfaceError(Exception):
    def __str__(self):
        return 'This interface was already added'


class UnknowInterfaceError(ExceptionFmt):
    def __init__(self, value):
        super(UnknowInterfaceError, self).__init__('Invalid or Unknown Interface type "{0!r}"', value)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class InterfaceManager
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class InterfaceManager(object):
    """

    """

    I2C, \
    SPI, \
    PWM, \
    GPIO, \
    SERIAL, \
    I2CSLAVE, \
    SPISLAVE = range(0xF1, 0xF8)

    def __init__(self, mode=gpio.BCM, debug=False):

        self._debug = debug
        self._interfaces = {}

        self.model = gpio.RPI_INFO['TYPE']
        self.revision = gpio.RPI_INFO['P1_REVISION']
        self.hardware = ' :: '.join((gpio.RPI_INFO['PROCESSOR'], gpio.RPI_INFO['RAM']))

        gpio.setwarnings(debug)
        gpio.cleanup()
        gpio.setmode(mode)

        # Alias functions for backward compatibility
        setattr(self, 'add_interface', self.append)
        setattr(self, 'del_interface', self.delete)

    def setup(self, pin, mode, initial, callback, pud, edge, bouncetime):
        """  """

        if not isinstance(pin, (int, long)):
            raise InvalidTypeError('The "pin"', 'numeric')

        def check_in_use(pin, modes):
            for mode in modes:
                if not mode in self._interfaces:
                    continue

                if not hasattr(self._interfaces[mode], '__iter__'):
                    if pin in self._interfaces[mode]:
                        raise InUseChannelError(pin, self._interfaces[mode], self._interfaces[mode].get_name())
                else:
                    for iface in self._interfaces[mode]:
                        if pin in iface:
                            raise InUseChannelError(pin, iface, iface.get_name())

        if mode == gpio.OUT:
            check_in_use(pin, (self.I2C, self.SPI, self.PWM, self.GPIO))
            gpio.setup(pin, mode, gpio.PUD_OFF, initial)

        elif mode == gpio.IN:
            check_in_use(pin, (self.I2C, self.SPI, self.PWM, self.GPIO))
            gpio.setup(pin, mode, pud or gpio.PUD_DOWN)
            gpio.add_event_detect(pin, edge or gpio.BOTH, callback, bouncetime)

        else:
            raise InvalidModeChannelError(pin)


    def get_mode(self):
        """ Returns the numbering mode of GPIO channels. """

        return gpio.get_mode()


    def get_connection(self, iface):
        """ Returns the connection bus depending on the class that is passed. """

        if isinstance(iface, InterfaceGPIO):
            return gpio

        else:
            raise UnknowInterfaceError(iface.__class__)


    def cleanup(self, pin=None):
        """ Clean the configuration of the one or more channels. """

        if pin == None:
            if any(self._interfaces.values()):
                logger.warn('There are still active Interfaces in InterfaceManager')

            gpio.cleanup()

        else:
            mode = gpio.gpio_function(pin)

            if mode == gpio.OUT:
                gpio.cleanup(pin)

            elif mode == gpio.IN:
                gpio.cleanup(pin)
                gpio.remove_event_detect(pin)

            elif mode == gpio.I2C:
                raise NotImplementedError()

            elif mode == gpio.SPI:
                raise NotImplementedError()

            elif mode == gpio.HARD_PWM:
                raise NotImplementedError()

            elif mode == gpio.SERIAL:
                raise NotImplementedError()

            else:
                raise UnknowTypeChannelError()


    def append(self, iface):
        """ Add an interface of the InterfaceManager. """

        if isinstance(iface, InterfaceGPIO):
            if not self.GPIO in self._interfaces:
                self._interfaces[self.GPIO] = []

            if iface in self._interfaces[self.GPIO]:
                raise DuplicateInterfaceError()

            self._interfaces[self.GPIO].append(iface)

        else:
            UnknowInterfaceError(iface.__class__)


    def delete(self, iface):
        """ Delete an interface of the InterfaceManager. """

        if isinstance(iface, InterfaceGPIO):
            if not self.GPIO in self._interfaces:
                return

            if not iface in self._interfaces[self.GPIO]:
                raise NotFoundInterfaceError()

            self._interfaces[self.GPIO].remove(iface)

        else:
            UnknowInterfaceError(iface.__class__)
