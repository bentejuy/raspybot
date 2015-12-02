#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         exceptions
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/19/2015
# Modified:     11/29/2015
# Version:      0.0.53
# Copyright:    (c) 2012-2015 Bentejuy Lopez
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

import exceptions

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Common Exceptions
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class ExceptionFmt(Exception):
    def __init__(self, *args):
        self.__expr__ = args[0]
        self.__args__ = args[1:]

    def __str__(self):
        return self.__expr__.format(*self.__args__)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class UnknowTypePortError(RuntimeWarning):
    def __str__(self):
        return 'Unknown mode type port'


class DuplicateInterfaceError(Exception):
    def __str__(self):
        return 'This interface was already added'


class NotFoundInterfaceError(Exception):
    def __str__(self):
        return 'Inteface not found'


class UnknowMotorModeError(Exception):
    def __str__(self):
        return 'Invalid or Unknown mode motor type'


class IsRunningError(ExceptionFmt):
    def __init__(self, name, details):
        super(IsRunningError, self).__init__('{} must be stopped to change {}', name, details)


class InvalidInterfaceError(Exception):
    def __str__(self):
        return 'The interface must be a valid "Interface" object'


class InterfaceTypeMustBe(ExceptionFmt):
    def __init__(self, name, value):
        super(InterfaceTypeMustBe, self).__init__('The "{0}" parameter must be a valid {1} class ', name, value)


class InterfaceSizeMustBe(ExceptionFmt):
    def __init__(self, name, value, details=''):
        super(InterfaceSizeMustBe, self).__init__('The number of channels in the interface {0} must be equal or higher {1}', name, value, details)


class InterfaceNoSupported(ExceptionFmt):
    def __init__(self, name, value):
        super(InterfaceNoSupported, self).__init__('The "{0}" does not support the interface {1} class', name, value)


class NoChannelInterfaceError(ExceptionFmt):
     def __init__(self, name, details):
        super(NoChannelInterfaceError, self).__init__('The Interface not have the channel {0} in channels {1} list', name, details)


class OutRangeError(ExceptionFmt):
    def __init__(self, name, details=''):
        super(OutRangeError, self).__init__('The {0} is out of range {1}', name, details)


class InvalidFunctionError(ExceptionFmt):
    def __init__(self, func):
        super(InvalidFunctionError, self).__init__('The parameter "{0}" must be a valid function or None', func)


class InvalidTypeError(ExceptionFmt):
    def __init__(self, name, condition, details=''):
        super(InvalidTypeError, self).__init__('{0} must be a valid {1} value {2}', name, condition, details)


class InvalidRangeError(ExceptionFmt):
    def __init__(self, value):
        super(InvalidRangeError, self).__init__('The "{0}" parameter must be a tuple or list with the range of minimum and maximum {0} to work', value)


class MinMaxValueError(ExceptionFmt):
    def __init__(self, name, var, condition, value):
        super(MinMaxValueError, self).__init__('The "{0}" {1} value must be {2} than the {3}', name, var, condition, value)

