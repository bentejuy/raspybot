#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         interfacemanager
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/07/2015
# Modified:     05/26/2015
# Version:      0.0.63
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

try:
    from smbus import SMBus as smbus

except ImportError:
    smbus = False

from ..interface import gpio
from ..interface import DuplicateInterfaceError, UnknowTypePortError, NotFoundInterfaceError, InvalidFunctionError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class InterfaceManager
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class InterfaceManager(object):
    def __init__(self, mode=gpio.BCM, warning=False):
        self._model = None
        self._hardware = None
        self._revision = None
        self._interfaces = []

        gpio.setwarnings(False)
        gpio.cleanup()
        gpio.setmode(mode)

        self._revision = gpio.RPI_REVISION

        with open('/proc/cpuinfo', 'r') as info:
            for line in info:
                line = line.strip(' \n\r\t')

                if not line:
                    continue

                try:
                    key, value = line.split(':', 2)

                    if 'Model' in key:
                        self._model = value
                    elif 'Hardware' in key:
                        self._hardware = value
                except Exception, e:
                    logger.error('Error reading in cpuinfo file: %s' % line)


    def setup(self, pin, mode, initial, callback, pud, edge, bouncetime):
        if mode == gpio.OUT:
            gpio.setup(pin, mode, gpio.PUD_OFF, initial)

        elif mode == gpio.IN:
            gpio.setup(pin, mode, pud or gpio.PUD_DOWN)

            if callback:
                if not hasattr(callback, '__call__'):
                    raise InvalidFunctionError('callback')

                gpio.add_event_detect(pin, edge or gpio.BOTH, callback, bouncetime)

        elif mode == gpio.ALT0:
            pass

        else:
            raise Exception('Configuring port "{0}" in an invalid mode.'.format(pin))


    def cleanup(self, pin=None):
        if pin == None:
            gpio.cleanup()
        else:
            mode = gpio.gpio_function(pin)

            if mode == gpio.OUT:
                gpio.cleanup(pin)

            elif mode == gpio.IN:
                gpio.cleanup(pin)
                gpio.remove_event_detect(pin)

            elif mode == gpio.SPI:
                raise NotImplementedError()
            elif mode == gpio.I2C:
                raise NotImplementedError()
            elif mode == gpio.PWM:
                raise NotImplementedError()
            elif mode == gpio.SERIAL:
                raise NotImplementedError()
            else:
                raise UnknowTypePortError()


    def add_interface(self, iface):
        if iface in self._interfaces:
            raise DuplicateInterfaceError()

        self._interfaces.append(iface)


    def del_interface(self, iface):
        if not iface in self._interfaces:
            raise NotFoundInterfaceError()

        self._interfaces.remove(iface)
#        del iface


