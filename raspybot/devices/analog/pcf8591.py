#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         pcf8591
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/19/2016
# Modified:     01/24/2016
# Version:      0.0.29
# Copyright:
# Licence:      GLPv3
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from time import sleep

from ..analogic import Device
from ..analogic import InterfaceI2CSlave
from ..analogic import InterfaceNoSupported, OutRangeError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class PCF8591
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class PCF8591(Device):
    """

    """

    ADC0, \
    ADC1, \
    ADC2, \
    ADC3, \
    ADC_WRITE = range(5)

    DAC_ENABLE = 0x40
    DAC_DISABLE = 0x00


    def __init__(self, iface, mode=2, name=None):

        if not isinstance(iface, InterfaceI2CSlave):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        if iface.get_address() < 0x48 or iface.get_address() > 0x4F:
            raise Exception('The PCF8591 need an i2c interface with an address between 0x48 and 0x4F')

        super(PCF8591, self).__init__(iface, name)

        self._values = [0, 0, 0, 0]
        self._reading = False

        self._iface.set_callback(self.__read_data__)


    def __wait_reply__(self, timeout=0.01):
        if self._reading is False:
            return True

        else:
            timeout = timeout / 10.0

            for tries in range(10):
                if self._reading is False:
                    return True

                sleep(timeout)

        return False


    def __read_data__(self, addr, comm, data):
        if comm >= self.ADC0 or comm <= self.ADC3:
            self._values[comm] = data >> 8

        self._reading = False


    def enableDAC(self):
        """  """
        self._iface.write_byte(self.DAC_ENABLE)


    def disableDAC(self):
        """  """
        self._iface.write_byte(self.DAC_DISABLE)


    def read(self, channel):
        """  """

        if channel < 0 or channel > 3:
            raise OutRangeError('channel')

        if self.__wait_reply__():
            self._reading = self.ADC0 + channel

            self._iface.write(channel)
            sleep(0.0001)
            self._iface.read_to(channel, 2)

            if self.__wait_reply__():
                return self._values[channel]

        return False


    def write(self, value):
        """  """

        if self.__wait_reply__():
            self._reading = self.ADC_WRITE

            try:
                if isinstance(value, int):
                    self._iface.write_byte(value, self.DAC_ENABLE)

                elif isinstance(value, (tuple, list)):
                    offset = 0
                    length = len(value)

                    while offset < length:
                        self._iface.write_to(self.DAC_ENABLE, value[offset : offset + 32], 32)
                        offset += 32

                else:
                    return False

            finally:
                self._reading = False

            return True

        return False

