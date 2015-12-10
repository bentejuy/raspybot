#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tasksi2c
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      10/29/2015
# Modified:     12/10/2015
# Version:      0.0.17
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

from ..task import Task

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
#  -. Class TaskI2C
#
#   @parameters :
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class TaskI2C(Task):
    I2C_READ, \
    I2C_READ_BYTE, \
    I2C_READ_WORD, \
    I2C_READ_BLOCK, \
    I2C_WRITE, \
    I2C_WRITE_BYTE, \
    I2C_WRITE_WORD, \
    I2C_WRITE_BLOCK, \
    I2C_READ_ERROR, \
    I2C_WRITE_ERROR, \
    I2C_READ_SUCCESS, \
    I2C_WRITE_SUCCESS = range(12)

    def __init__(self, action, address, data, comm=0, length=None, timeout=-1):
        super(TaskI2C, self).__init__(timeout)

        self.comm = comm
        self.data = data
        self.action = action
        self.length = length
        self.address = address


    def __str__(self):
        return '{} => action: {} :: data: {} :: address: {} :: started: {}'.format(self.__class__, self.action, self.data, self.address, self._started)
