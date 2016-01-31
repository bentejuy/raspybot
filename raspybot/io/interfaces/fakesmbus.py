#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         fakesmbus
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      12/07/2015
# Modified:     01/24/2016
# Version:      0.0.07
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
#   Constants
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

FAKE = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
#   Class SMBus
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class SMBus(object):


    def __init__(self, bus=-1):
        self._pec = False
        logger.debug('Initializing smbus {}'.format(bus))


    def close(self):
        logger.debug('Closing I2C bus...')


    def dealloc(self):
        self.close()


    def open(self, bus):
        logger.debug('Open I2C bus number {0:#X}'.format(bus))


    def write_quick(self, addr):
        logger.debug('Calling the method "write quick" on I2C bus {0:#X}'.format(addr))


    def read_byte(self, addr):
        logger.debug('Reading byte on I2C bus {0:#X}'.format(addr))

        return 0


    def write_byte(self, addr, val):
        logger.debug('Writing a byte on I2C bus {0:#X}, value => {1}'.format(addr, val))


    def read_byte_data(self, addr, cmd):
        logger.debug('Reading a byte data transaction on I2C bus {0:#X} :: cmd => {1}'.format(addr, cmd))

        return 0


    def write_byte_data(self, addr, cmd, val):
        logger.debug('Writing a byte data transaction on I2C bus {0:#X} :: cmd => {1} :: value => {2}'.format(addr, cmd, val))


    def read_word_data(self, addr, cmd):
        logger.debug('Reading a word data transaction on I2C bus {0:#X} :: cmd => {1}'.format(addr, cmd))

        return 0


    def write_word_data(self, addr, cmd, val):
        logger.debug('Writing a word data transaction on I2C bus {0:#X} :: cmd => {1} :: value => {2}'.format(addr, cmd, val))


    def process_call(self, addr, cmd, val):
        logger.debug('Writing and Reading 16 bits on I2C bus {0:#X} :: cmd => {1} :: value => {2}'.format(addr, cmd, val))

        return 0


    def read_block_data(self, addr, cmd):
        logger.debug('Reading block data transaction on I2C bus {0:#X} :: cmd => {1}'.format(addr, cmd))

        return 0


    def write_block_data(self, addr, cmd, vals):
        logger.debug('Writing a block data transaction on I2C bus {0:#X} :: cmd => {1} :: value => {2}'.format(addr, cmd, vals))


    def block_process_call(self, addr, cmd, vals):
        logger.debug('Writing and Reading a block data transaction on I2C bus {0:#X} :: cmd => {1} :: value => {2}'.format(addr, cmd, vals))

        return 0


    def read_i2c_block_data(self, addr, cmd, len=32):
        logger.debug('Reading block data transaction on I2C bus {0:#X} :: cmd => {1}'.format(addr, cmd))

        return 0


    def write_i2c_block_data(self, addr, cmd, vals):
        logger.debug('Writing a block data transaction on I2C bus {0:#X} :: cmd => {1} :: value => {2}'.format(addr, cmd, vals))


    @property
    def pec(self):
        return self._pec


    @pec.setter
    def pec(self, value):
        """True if Packet Error Codes (PEC) are enabled"""
        self._pec = bool(value)
