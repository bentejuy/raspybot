#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         fakegpio
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/17/2015
# Modified:     05/21/2015
# Version:      0.0.43
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class fakeGPIO
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class fakeGPIO(object):
    BCM = 11
    SPI = 41
    I2C = 42
    BOARD = 10
    SERIAL = 40
    UNKNOWN = -1
    HARD_PWM = 43

    IN = 1
    OUT = 0
    ALT0 = 4

    LOW = 0
    HIGH = 1
    PUD_UP =  2 + 20
    PUD_OFF =  0 + 20
    PUD_DOWN = 1 + 20

    BOTH = 3 + 30
    RISING = 1 + 30
    FALLING = 2 + 30

    INFO = {}
    VERSION = "0.5.11a"
    RPI_REVISION = 0x03

    def __init__(self):
        self._mode = self.BCM


    def setmode(self, mode):
        if not mode in (self.BCM, self.BOARD):
            raise Exception('The valid modes only can be BCM or BOARD')

        self._mode = mode


    def getmode(self):
        return self._mode


    def setwarnings(self, action):
        pass


    def setup(self, pin, mode, initial=None, callback=None, pud=None, edge=None, bouncetime=200):
        msg = [pin]
        msg.append(self._mode == self.BCM and 'BCM' or 'BOARD')

        if mode == self.IN:
            msg.append('Input' + (callback <> None and (' with function call : {}'.format(callback)) or ''))

        elif mode == self.OUT:
            msg.append('Output' + (initial <> None and (' with value : {}'.format(initial)) or ''))

        elif mode == self.ALT0:
            msg.append('ALT0')

        else:
            logger.error('Configuring channel "{}" in an invalid mode.'.format(pin))

        logger.debug('Configuring channel {} ({}) in mode {}'.format(*msg))


    def input(self, pin):
        logger.debug('Reading in channel {} =>'.format(pin))


    def output(self, pin, data):
        logger.debug('Writing in channel {0} => {1} (0x{1:x}, 0b{1:b})'.format(pin, data))


    def gpio_function(self, pin):
        pass


    def add_event_detect(self, pin, edge, callback, bouncetime):
        logger.debug('Added event in channel {0} with detecting edje {1} and {2}ms of bouncetime'.format(pin, edge, bouncetime))


    def cleanup(self, pin=None):
        if pin == None:
            logger.debug('Cleaning all GPIO channels')
        elif isinstance(pin, (int, long)):
            logger.debug('Cleaning channel "%d"' % pin)
        elif isinstance(pin, (tuple, list)):
            logger.debug('Cleaning channels [%s]' % ','.join(map(str, pin)))
        else:
            raise Exception('Invalid channel type, must be a intenger, tuple or list of integer numbers')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

FakeGPIO = fakeGPIO()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
