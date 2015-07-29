#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         buttons
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      04/01/2015
# Modified:     06/07/2015
# Version:      0.0.27
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

from ..button import gpio, Device
from ..button import InvalidFunctionError, NoChannelInterfaceError, InterfaceNoSupported

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class Buttons
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class Buttons(Device):
    """ Supervise the state of one or more inputs channels  when they change the state to up or down.
        It calls a callback function and passes the channel that generated the event and the new channel status. """

    CLICKED, \
    PRESSED, \
    RELEASE = range(3)

    PUD_UP = gpio.PUD_UP
    PUD_DOWN = gpio.PUD_DOWN

    def __init__(self, iface, name=None, clicked=None, pressed=None, release=None):

        if not isinstance(iface, InterfaceGPIO):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        super(Buttons, self).__init__(iface, name)

        if not any((clicked, pressed, release)):
            raise Exception('The button object needs at least a callback to work')

        if clicked and not hasattr(clicked, '__call__'):
            raise InvalidFunctionError('clicked')

        if pressed and not hasattr(pressed, '__call__'):
            raise InvalidFunctionError('pressed')

        if release and not hasattr(release, '__call__'):
            raise InvalidFunctionError('release')

        self._on_clicked = clicked
        self._on_pressed = pressed
        self._on_release = release


    def __on_clicked__(self, pin):
        if not self._on_clicked:
            logger.error('The "clicked" callback was not defined')
        else:
            self._on_clicked(self, pin, self.CLICKED)


    def __on_pressed__(self, pin):
        if not self._on_pressed:
            logger.error('The "pressed" callback was not defined')
        else:
            self._on_pressed(self, pin, self.PRESSED)


    def __on_release__(self, pin):
        if not self._on_release:
            logger.error('The "release" callback was not defined')
        else:
            self._on_release(self, pin, self.RELEASE)


    def setup(self, pin, event, pud=gpio.PUD_UP, bouncetime=200):
        iface = self.get_interface()

        if not pin in iface.get_in_ports():
            raise NoChannelInterfaceError(pin, 'input')

        try:
            edge, callback = {self.CLICKED: (gpio.RISING, self.__on_clicked__),
                              self.PRESSED: (gpio.BOTH, self.__on_pressed__),
                              self.RELEASE: (gpio.FALLING, self.__on_release__)}[event]

            iface.setup(pin, gpio.IN, 0, callback, pud, edge, bouncetime)

        except KeyError:
            raise Exception('Configuring channel {0} in an invalid event mode.'.format(pin))

