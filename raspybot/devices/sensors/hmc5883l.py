#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         hmc5883l
# Purpose:      3 axis digital compass
#
# Author:       Bentejuy Lopez
# Created:      01/31/2016
# Modified:     02/21/2016
# Version:      0.0.27
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import logging

from time import sleep

from ..sensor import Device
from ..sensor import InterfaceI2CSlave
from ..sensor import InterfaceNoSupported, OutRangeError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class HMC5883L
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class HMC5883L(Device):
    """

    """

    # gauss -> register, scale
    SCALES = { 0.88: (0x00, 0.73),
               1.3 : (0x20, 0.92),
               1.9 : (0x40, 1.22),
               2.5 : (0x60, 1.52),
               4.0 : (0x80, 2.27),
               4.7 : (0xA0, 2.56),
               5.6 : (0xC0, 3.03),
               8.1 : (0xE0, 4.35)}

    CFG_REGA = 0x00
    CFG_REGB = 0x01
    SET_MODE = 0x02
    MEASURES = 0x03

    IDLE = 0x02
    SINGLE = 0x01
    CONTINUOS = 0x00

    OUTPUT_RATES = (0.75, 1.5, 3, 7.5, 15, 30, 75)


    def __init__(self, iface, name=None):
        super(HMC5883L, self).__init__(iface, name)

        if not isinstance(iface, InterfaceI2CSlave):
            raise InterfaceNoSupported(self.__class__, iface.__class__)

        if iface.get_address() != 0x1E:
            raise Exception('The HMC5883L need an i2c interface with the address 0x1E')

        self._mode = self.SINGLE
        self._scale = 0.92
        self._values = [0, 0, 0]
        self._reading = False

        self._iface.set_callback(self.__read_data__)


    def __wait_reply__(self, timeout=0.01):
        if not self._reading:
            return True

        else:
            timeout /=  10.0

            for tries in range(10):
                if not self._reading:
                    return True

                sleep(timeout)

        return False


    def __read_data__(self, addr, comm, data):
        if comm == self.MEASURES:
            x_axis = data[1] | data[0] << 8
            z_axis = data[3] | data[2] << 8
            y_axis = data[5] | data[4] << 8

            for idx, val in enumerate((x_axis, y_axis, z_axis)):
                if val >= 0x8000:
                    val = -((0xFFFF - val) + 1)

                self._values[idx] = round(val * self._scale, 3)


    def set_mode(self, mode):
        """  """

        if not mode in (self.CONTINUOS, self.IDLE, self.SINGLE):
            raise OutRangeError('Read Mode')

        self._mode = mode
        self._iface.write_byte(mode, self.SET_MODE)


    def set_rate(self, hz):
        """  """

        if self._mode != self.CONTINUOS:
            return

        if not hz in self.OUTPUT_RATES:
            logger.warn('*** :'.join(map(str, self.OUTPUT_RATES)))

        self._iface.write_byte(self.OUTPUT_RATES.index(hz) << 2, self.CFG_REGA)


    def set_scale(self, gauss):
        """  """

        try:
            reg, scale= self.SCALES[gauss]

            self._scale = scale
            self._iface.write_byte(reg, self.CFG_REGB)

        except KeyError:
            logger.warn('Gauss values must be one of the following values :'.join(map(str, self.SCALES)))


    def get_scaleAxis(self):
        """  """

        self._iface.read_to(self.MEASURES, 6)

        if self._mode == self.CONTINUOS:
            sleep(0.005)

        if self.__wait_reply__():
            return self._values

        return None

