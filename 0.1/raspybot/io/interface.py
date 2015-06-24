#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         interface
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/07/2015
# Modified:     04/02/2015
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
"""
        WorkerTask
            |
            |
        Interface
            |
            |---> InterfaceGPIO
            |
            |---> InterfaceSPI
            |
            |---> InterfaceI2C
            |
            |---> InterfaceNet


        InterfaceManager
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

try:
    import RPi.GPIO as gpio

except ImportError:
    from interfaces.fakegpio import FakeGPIO as gpio

from .task import TaskGPIO
from ..utils.worker import WorkerTask
from ..utils.exceptions import InvalidTypeError, InvalidFunctionError, UnknowTypePortError, DuplicateInterfaceError, UnknowTypePortError, NotFoundInterfaceError

from interfaces.interface import Interface
from interfaces.interfacegpio import InterfaceGPIO
from interfaces.interfacemanager import InterfaceManager

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

