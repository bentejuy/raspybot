#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         interface
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/07/2015
# Modified:     01/29/2016
# Version:      0.0.85
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
        Interface
            |
            |
        InterfaceActive
            |
            |---> InterfaceGPIO
            |
            |---> InterfacePWM
            |
            |---> InterfaceSPIMaster
            |
            |---> InterfaceI2CMaster
            |
            |
        InterfaceSlave
            |
            |---> InterfaceSPISlave
            |
            |---> InterfaceI2CSlave


        InterfaceManager
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

try:
    import RPi.GPIO as gpio

except ImportError:
    from .interfaces import fakegpio as gpio
#    logger.warn('Initializing "InterfaceManager" in debug mode because RPi.GPIO module was not found')

try:
    import smbus

except ImportError:
    from .interfaces import fakesmbus as smbus
#    logger.warn('Error importing the "smbus" module, using the "fakesmbus" module  by default')


from .task import TaskPWM
from .task import TaskI2C
from .task import TaskGPIO

from ..core.worker import WorkerTask
from ..core.exceptions import InvalidTypeError, InvalidFunctionError, InvalidInterfaceError, \
                              OutRangeError, ExceptionFmt

from .interfaces.interface import Interface
from .interfaces.interface import InterfaceSlave
from .interfaces.interface import InterfaceActive
from .interfaces.interfacepwm import InterfacePWM
from .interfaces.interfacegpio import InterfaceGPIO
from .interfaces.interfacei2c import InterfaceI2CSlave
from .interfaces.interfacei2c import InterfaceI2CMaster
from .interfaces.interfacemanager import InterfaceManager

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
