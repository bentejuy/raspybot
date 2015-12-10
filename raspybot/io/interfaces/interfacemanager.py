#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         interfacemanager
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/07/2015
# Modified:     12/10/2015
# Version:      0.0.91
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
from ..interface import smbus

from ..interface import InterfacePWM
from ..interface import InterfaceGPIO
from ..interface import InterfaceI2CSlave
from ..interface import InterfaceI2CMaster

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
    def __init__(self, channel, iface):
        super(InUseChannelError, self).__init__('The channel {0} is in use by interface class {1})', channel, iface)


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


class NoMasterInterfaceError(ExceptionFmt):
    def __init__(self, value):
        super(NoMasterInterfaceError, self).__init__('The {0} Slave Interface needs to have previously created a {0} Master Interface"', value)


class OnlyOneInterfaceError(ExceptionFmt):
    def __init__(self, value):
        super(OnlyOneInterfaceError, self).__init__('There only can be one Interface "{0}"', value)


class DuplicateAddressI2CError(ExceptionFmt):
    def __init__(self, value):
        super(DuplicateAddressI2CError, self).__init__('The address "{0:#X}" on the I2C bus is already in use"', value)


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


    def setup(self, pin, mode, initial=0, callback=None, pud=gpio.PUD_DOWN, edge=gpio.BOTH, bouncetime=200, owner=None):
        """  """

        if not isinstance(pin, (int, long)):
            raise InvalidTypeError('The "pin"', 'numeric')

        def check_in_use(pin, modes, owner):
            for mode in modes:
                if not mode in self._interfaces:
                    continue

                if not hasattr(self._interfaces[mode], '__iter__'):
                    if pin in self._interfaces[mode]:
                        if owner and owner is self._interfaces[mode]:
                            return

                        raise InUseChannelError(pin, self._interfaces[mode].__class__)
                else:
                    for iface in self._interfaces[mode]:
                        if pin in iface:
                            if owner and owner is iface:
                                return

                            raise InUseChannelError(pin, iface.__class__)

        if mode == gpio.OUT:
            check_in_use(pin, (self.I2C, self.SPI, self.PWM, self.GPIO), owner)
            gpio.setup(pin, mode, gpio.PUD_OFF, initial)

        elif mode == gpio.IN:
            check_in_use(pin, (self.I2C, self.SPI, self.PWM, self.GPIO), owner)
            gpio.setup(pin, mode, pud)

            if hasattr(callback, '__call__'):
                gpio.add_event_detect(pin, edge, callback, bouncetime)

        elif mode == gpio.HARD_PWM:
            check_in_use(pin, (self.I2C, self.SPI, self.PWM, self.GPIO), owner)
            gpio.setup(pin, gpio.OUT, gpio.PUD_OFF, initial)

        elif mode == gpio.I2C:
            check_in_use(pin, (self.SPI, self.PWM, self.GPIO), owner)

        else:
            raise InvalidModeChannelError(pin)


    def get_mode(self):
        """ Returns the numbering mode of GPIO channels. """
        return gpio.getmode()


    def get_connection(self, iface):
        """ Returns the connection bus depending on the class that is passed. """

        if isinstance(iface, InterfaceGPIO):
            return gpio

        elif isinstance(iface, InterfacePWM):
            return gpio

        elif isinstance(iface, InterfaceI2CMaster):
            if hasattr(smbus, 'fake') and not self._debug:
                raise ImportError('Error loading the module python-smbus, set to "True" the debug parameter to load the fakeSMBus module to make tests or install the python-smbus module')

            return smbus.SMBus()

        elif isinstance(iface, InterfaceI2CSlave):
            if not self._interfaces[self.I2C]:
                raise NoMasterInterfaceError('I2C')

            return self._interfaces[self.I2C]

        else:
            raise UnknowInterfaceError(iface.__class__)


    def cleanup(self, pin=None):
        """ Clean the configuration of one or more channels. """

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
                pass

            elif mode == gpio.SPI:
                raise NotImplementedError()

            elif mode == gpio.HARD_PWM:
                gpio.cleanup(pin)

            elif mode == gpio.SERIAL:
                raise NotImplementedError()

            else:
                raise UnknowTypeChannelError()


    def append(self, iface):
        """ Add an interface to the InterfaceManager. """

        if isinstance(iface, InterfaceGPIO):
            if not self.GPIO in self._interfaces:
                self._interfaces[self.GPIO] = []

            if iface in self._interfaces[self.GPIO]:
                raise DuplicateInterfaceError()

            self._interfaces[self.GPIO].append(iface)

        elif isinstance(iface, InterfacePWM):
            if not self.PWM in self._interfaces:
                self._interfaces[self.PWM] = []

            if iface in self._interfaces[self.PWM]:
                raise DuplicateInterfaceError()

            self._interfaces[self.PWM].append(iface)

        elif isinstance(iface, InterfaceI2CMaster):
            if self.I2C in self._interfaces:
                raise OnlyOneInterfaceError(iface.__class__)

            self._interfaces[self.I2C] = iface

        elif isinstance(iface, InterfaceI2CSlave):
            if not self.I2C in self._interfaces:
                raise NoMasterInterfaceError('I2C')

            try:
                self._interfaces[self.I2C].register(iface)

            except KeyError:
                raise DuplicateAddressI2CError(iface.get_address())

        else:
            UnknowInterfaceError(iface.__class__)


    def delete(self, iface):
        """ Delete an interface to the InterfaceManager. """

        if isinstance(iface, InterfaceGPIO):
            if not self.GPIO in self._interfaces:
                return

            if not iface in self._interfaces[self.GPIO]:
                raise NotFoundInterfaceError()

            iface.free()
            self._interfaces[self.GPIO].remove(iface)

        elif isinstance(iface, InterfacePWM):
            if not self.PWM in self._interfaces:
                return

            if not iface in self._interfaces[self.PWM]:
                raise NotFoundInterfaceError()

            iface.free()
            self._interfaces[self.PWM].remove(iface)

        elif isinstance(iface, InterfaceI2CMaster):
            if not self.I2C in self._interfaces:
                return

            if not iface is self._interfaces[self.I2C]:
                raise NotFoundInterfaceError()

            iface.free()
            del self._interfaces[self.I2C]

        elif isinstance(iface, InterfaceI2CSlave):
            if not self.I2C in self._interfaces:
                return

            try:
                self._interfaces[self.I2C].remove(iface)

            except KeyError:
                raise NotFoundInterfaceError()

        else:
            UnknowInterfaceError(iface.__class__)
