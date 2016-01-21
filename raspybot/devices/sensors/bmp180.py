#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         bmp180
# Purpose:      Read data from digital pressure sensor BMP180
#
# Author:       Bentejuy Lopez
# Created:      01/16/2016
# Modified:     01/21/2016
# Version:      0.0.27
# Copyright:
# Licence:      GLPv3
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from time import sleep
from struct import pack, unpack

from ..sensor import Device
from ..sensor import InterfaceI2CSlave
from ..sensor import InterfaceNoSupported

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class BMP180
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class BMP180(Device):
    """

    """

    AC1, \
    AC2, \
    AC3, \
    AC4, \
    AC5, \
    AC6, \
    B1, \
    B2, \
    MB, \
    MC, \
    MD = range(11)

    CONTROL = 0xF4
    MEASURES = 0xF6
    PRESSURE = 0X34
    TEMPERATURE = 0X2E
    CALIBRATION = 0xAA
    INFORMATION = 0xD0

    def __init__(self, iface, mode=2, name=None):

        if not isinstance(iface, InterfaceI2CSlave):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        if iface.get_address() != 0x77:
            raise Exception('The BMP180 need an i2c interface with the address 0x77')

        super(BMP180, self).__init__(iface, name)

        self._iface.set_callback(self.__read_data__)

        self._id = None
        self._version = None

        self._B5 = 0
        self._mode = 1
        self._cald = None
        self._pres = None
        self._temp = None
        self._delay = (0.005, 0.01, 0.015, 0.03)
        self._reading = False

        self._iface.read_to(self.INFORMATION, 2)
        self._iface.read_to(self.CALIBRATION, 22)


    def __read_data__(self, addr, comm, data):
        if comm == self.INFORMATION:
            self._id, \
            self._version = unpack('bb', pack('h', data))

        elif comm == self.CALIBRATION:
            self._cald = unpack('>hhhHHHhhhhh', pack(''.rjust(22, 'B'), *data))


        elif comm == self.MEASURES:
            if self._reading == self.PRESSURE:
                data.reverse()
                raw = unpack('i', pack('BBB', *data) + '\x00')[0] >> (8 - self._mode)

                B6 = self._B5 - 4000
                X1 = (self._cald[self.B2] * (B6 * B6) >> 12) >> 11
                X2 = (self._cald[self.AC2] * B6) >> 11
                X3 = X1 + X2
                B3 = (((self._cald[self.AC1] * 4 + X3) << self._mode) + 2) / 4
                X1 = (self._cald[self.AC3] * B6) >> 13
                X2 = (self._cald[self.B1] * ((B6 * B6) >> 12)) >> 16
                X3 = ((X1 + X2) + 2) >> 2
                B4 = (self._cald[self.AC4] * (X3 + 32768)) >> 15
                B7 = (raw - B3) * (50000 >> self._mode)

                if B7 < 0x80000000:
                    PS = (B7 * 2) / B4
                else:
                    PS = (B7 / B4) * 2

                X1 = (PS >> 8) * (PS >> 8)
                X1 = (X1 * 3038) >> 16
                X2 = (-7357 * PS) >> 16

                self._pres = (PS + ((X1 + X2 + 3791) >> 4)) / 100.0

            elif self._reading == self.TEMPERATURE:
                raw = data >> 8 | (data & 0xFF) << 8

                X1 = ((raw - self._cald[self.AC6]) * self._cald[self.AC5]) >> 15
                X2 = (self._cald[self.MC] << 11) / (X1 + self._cald[self.MD])
                B5 = X1 + X2

                self._B5 = B5
                self._temp = ((B5 + 8) >> 4) / 10.0

        self._reading = False


    def __read_pressure__(self):
        self._iface.write_byte(self.PRESSURE | (self._mode << 6), self.CONTROL)
        sleep(self._delay[self._mode])
        self._reading = self.PRESSURE
        self._iface.read_to(self.MEASURES, 3)


    def __read_temperature__(self):
        self._reading = self.TEMPERATURE
        self._iface.write_byte(self.TEMPERATURE, self.CONTROL)
        sleep(0.005)
        self._reading = self.TEMPERATURE
        self._iface.read_to(self.MEASURES, 2)


    def set_mode(self, value):
        """  """

        if value < 0 or value > 3:
            raise OutRangeError('oversampling mode')

        self._mode = value


    def update(self, temperature=True, pressure=True):
        """  """

        if temperature or (pressure and self._B5 == 0):
            self.__read_temperature__()

        if pressure:
            self.__read_pressure__()


    def get_pressure(self, update=False):
        """  """

        if not update:
            return self._pres

        else:
            self.update(False, True)

            for tries in range(10):
                if not self._reading:
                    return self._pres

                sleep(0.01)

        return None


    def get_temperature(self, update=False):
        """  """

        if not update:
            return self._temp

        else:
            self.update(True, False)

            for tries in range(10):
                if not self._reading:
                    return self._temp

                sleep(0.01)

        return None
