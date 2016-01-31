#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tasks
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      10/14/2013
# Modified:     01/31/2016
# Version:      0.1.45
# Copyright:    (c) 2013-2016 Bentejuy Lopez
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

from time import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
#  -. Class Task
#
#    @parameters :
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class Task(object):
    WAITING, \
    RUNNING, \
    CONSTANT, \
    STOPPED, \
    TIMEOUT, \
    FINISHED = range(6)

    def __init__(self, timeout=0):
        self._state = self.CONSTANT if timeout < 0 else self.WAITING
        self._started = 0
        self._timeout = timeout


    @property
    def state(self):
        if self._state >= self.CONSTANT:
            return self._state

        if self._timeout and self._started:
            if self._started + self._timeout < time():
                self._state = self.TIMEOUT

        return self._state


    @state.setter
    def state(self, state):
        self._state = state

        if state == self.RUNNING:
            self._started = time()

            return self._timeout

        return 0
