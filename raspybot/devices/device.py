#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         device
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/16/2015
# Modified:     11/26/2015
# Version:      0.0.19
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import uuid

from ..io.interface import Interface
from ..utils.exceptions import InvalidInterfaceError, InvalidFunctionError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class Device
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class Device(object):
    """ The base class of all devices that interoperate with interfaces. """

    def __init__(self, iface, name=None):
        if not isinstance(iface, Interface):
            raise InvalidInterfaceError()

        self._name  = name or str(uuid.uuid4())
        self._iface = iface

    def __str__(self):
        return '{} :: name : {}'.format(self.__class__, self._name)


    def get_name(self):
        return self._name


    def get_interface(self):
        return self._iface


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class Device
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class ActionDevice(Device):
    """ The same as Device class, but with callback functions to supervise when it started and it stopped actions. """

    def __init__(self, iface, name, start=None, stop=None):
        super(ActionDevice, self).__init__(iface, name)

        if start and not hasattr(start, '__call__'):
            raise InvalidFunctionError('start')

        if stop and not hasattr(stop, '__call__'):
            raise InvalidFunctionError('stop')

        self._on_stop  = stop
        self._on_start = start


    def action_start(self):
        """ Calls the 'start' callback function if it was defined """
        if self._on_start:
            self._on_start(self)


    def action_stop(self):
        """ Calls the 'stop' callback function if it was defined """
        if self._on_stop:
            self._on_stop(self)

