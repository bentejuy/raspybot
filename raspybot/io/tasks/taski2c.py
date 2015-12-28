#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tasksi2c
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      10/29/2015
# Modified:     12/23/2015
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
    READ, \
    READ_BYTE, \
    READ_WORD, \
    READ_BLOCK, \
    QUERY, \
    QUERY_BYTE, \
    QUERY_WORD, \
    QUERY_BLOCK, \
    WRITE, \
    WRITE_BYTE, \
    WRITE_WORD, \
    WRITE_BLOCK, \
    READ_ERROR, \
    QUERY_ERROR, \
    WRITE_ERROR, \
    READ_SUCCESS, \
    QUERY_SUCCESS, \
    WRITE_SUCCESS = range(18)

    def __init__(self, action, address, data, comm=0, length=None, timeout=-1):
        super(TaskI2C, self).__init__(timeout)

        self.comm = comm
        self.data = data
        self.action = action
        self.length = length
        self.address = address


    def __str__(self):
        return '{} => action: {} :: data: {} :: address: {:#x} :: comm: {:#x} :: started: {}'.format(self.__class__, self.action, self.data, self.address, self.comm, self._started)
