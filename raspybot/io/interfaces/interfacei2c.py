#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         interfacei2c
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      10/26/2015
# Modified:     12/21/2015
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

from ..interface import gpio

from ..interface import TaskI2C
from ..interface import InterfaceSlave
from ..interface import InterfaceActive

from ..interface import InvalidFunctionError, OutRangeError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class InterfaceI2CSlave
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class InterfaceI2CSlave(InterfaceSlave):
    """

    """

    def __init__(self, manager, address, comm=0, success=None, failure=None):

        if not isinstance(address, (int, long)):
            raise TypeError('...')

        if address < 0x03 or address > 0x77:
            raise OutRangeError('address')

        self._comm = comm
        self._master = manager.get_connection(self)
        self._address = address

        if success and not hasattr(success, '__call__'):
            raise InvalidFunctionError('success')

        if failure and not hasattr(failure, '__call__'):
            raise InvalidFunctionError('failure')

        self._success = success
        self._failure = failure

        manager.append(self)


    def __success__(self, task):
        if self._success:
            self._success(task.address, task.data)


    def __failure__(self, task):
        if self._failure:
            self._failure(task.address, task.data)
        else:
            logger.error(task)


    def get_address(self):
        """  """
        return self._address


    def write(self, data):
        """  """
        self._master.append(TaskI2C(TaskI2C.I2C_WRITE_BYTE, self._address, data, self._comm))


    def write_to(self, data, comm=0, length=None):
        """  """

        if not length:
            task = TaskI2C(TaskI2C.I2C_WRITE if length is None else TaskI2C.I2C_WRITE_BYTE, self._address, data, comm)

        else:
            if isinstance(length, (int, long)) and length > 0:
                logger.critical('Type or value not valid in "length" parameter calling to method "write" on device {0:#x}'.format(self._address))
                return

            if length == 1:
                task = TaskI2C(TaskI2C.I2C_WRITE_BYTE, self._address, data)

            elif length == 2:
                task = TaskI2C(TaskI2C.I2C_WRITE_WORD, self._address, data, comm)

            else:
                task = TaskI2C(TaskI2C.I2C_WRITE_BLOCK, self._address, data, comm, length)

        self._master.append(task)


    def read(self, comm=None):
        """ """
        self._master.append(TaskI2C(TaskI2C.I2C_READ_BYTE, self._address, None, self._comm if comm is None else comm))


    def read_to(self, comm=0, length=None):
        """  """

        if not length:
            task = TaskI2C(TaskI2C.I2C_READ_BYTE if length is None else TaskI2C.I2C_READ_BYTE, self._address, data, comm)

        else:
            if isinstance(length, (int, long)) and length > 0:
                logger.critical('Type or value not valid in "length" parameter calling to method "read" on device {0:#x}'.format(self._address))
                return

            if length == 1:
                task = TaskI2C(TaskI2C.I2C_READ_BYTE, self._address, None)

            elif length == 2:
                task = TaskI2C(TaskI2C.I2C_REAd_WORD, self._address, None, comm)

            else:
                task = TaskI2C(TaskI2C.I2C_READ_BLOCK, self._address, None, comm, length)

        self._master.append(task)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class InterfaceI2CMaster
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class InterfaceI2CMaster(InterfaceActive):
    """

    """

    def __init__(self, manager):
        super(InterfaceI2CMaster, self).__init__(manager, self.__parser__)

        self._bus = manager.get_connection(self)
        self._slaves = {}
        self._manager = manager

        if self._manager.get_mode() == gpio.BOARD:
            self._pinout = (2, 3)
        else:
            self._pinout = (0, 1) if self._manager.revision >= 1 else (1, 2)

        self._bus.open(0 if self._manager.revision < 1 else 1)

        self._manager.setup(self._pinout[0], gpio.I2C)
        self._manager.setup(self._pinout[1], gpio.I2C)
        self._manager.append(self)


    def __contains__(self, item):
        if isinstance(item, (int, long)):
            return item in self._pinout_

        elif isinstance(item, InterfaceI2CSlave):
            return item.get_address() in self._slaves

        return False


    def __write__(self, task):
        try:
            if task.action == TaskI2C.I2C_WRITE:
                self._bus.write_byte(task.address, task.data)

            elif task.action == TaskI2C.I2C_WRITE_BYTE:
                self._bus.write_byte_data(task.address, task.comm, task.data)

            elif task.action == TaskI2C.I2C_WRITE_WORD:
                self._bus.write_word_data(task.address, task.comm, task.data)

            elif task.action == TaskI2C.I2C_WRITE_BLOCK:
                self._bus.write_i2c_block_data(task.address, task.comm, task.data)

        except IOError as error:
            self.__response__(TaskI2C.I2C_WRITE_ERROR, task, error)


    def __read__(self, task):
        try:
            if task.action == TaskI2C.I2C_READ:
                data = self._bus.read_byte(task.address)

            elif task.action == TaskI2C.I2C_READ_BYTE:
                data = self._bus.read_byte_data(task.address, task.comm)

            elif task.action == TaskI2C.I2C_READ_WORD:
                data = self._bus.read_word_data(task.address, task.comm)

            elif task.action == TaskI2C.I2C_READ_BLOCK:
                data = self._bus.read_i2c_block_data(task.address, task.comm, task.length if task.length else 32)

            else:
                logger.critical('Unknown I2C action reading :: Device => {0x%0.2x}'.format(task.address))

            self.__response__(TaskI2C.I2C_READ_SUCCESS, task, data)

        except IOError as error:
            self.__response__(TaskI2C.I2C_READ_ERROR, task, error)


    def __parser__(self, task):
        if task.action < TaskI2C.I2C_WRITE:
            self.__read__(task)

        elif task.action < TaskI2C.I2C_READ_ERROR:
            self.__write__(task)

        elif task.action < TaskI2C.I2C_READ_SUCCESS:
            try:
                self._slaves[task.address].__success__(task)

            except Exception as error:
                logger.critical(error)

        else:
            try:
                self._slaves[task.address].__failure__(task)

            except Exception as error:
                logger.critical(error)


    def __response__(self, action, task, data):
        task.data = data
        task.action = action

        super(self.__class__, self).__append__(task)

        if not self.alive():
            super(self.__class__, self).__start__()


    def __failure__(self, action, task, error):
        task.data = error
        task.action = action

        super(self.__class__, self).__append__(task)

        if not self.alive():
            super(self.__class__, self).__start__()


    def free(self):
        """  """

        try:
            self.__stop__()

        finally:
            self._bus.close()
            self._slaves.clear()


    def register(self, iface):
        """ Register a I2C slave interface to the master """

        if isinstance(iface, InterfaceI2CSlave):
            if iface.get_address() in self._slaves:
                raise KeyError

            self._slaves[iface.get_address()] = iface


    def remove(self, iface):
        """ Remove a I2C slave interface to the master """

        if isinstance(iface, InterfaceI2CSlave):
            del self._slaves[iface.get_address()]


    def append(self, task):
        """ Add a new task to the I2C interface queue """

        if isinstance(task, TaskI2C):
            super(self.__class__, self).__append__(task)

            if not self.alive():
                super(self.__class__, self).__start__()
        else:
            logger.critical('Error, adding a not valid task to I2C master interface')

