#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         motordc
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      07/23/2015
# Modified:     01/31/2016
# Version:      0.0.69
# Copyright:    (c) 2015-2016 Bentejuy Lopez
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
"""

    For more info see : https://www.youtube.com/watch?v=W7cV9_W12sM

"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from ..motor import Worker
from ..motor import MotorBase
from ..motor import InvalidTypeError, OutRangeError, IsRunningError, InvalidRangeError, \
                    MinMaxValueError, InterfaceNoSupported, InterfaceTypeMustBe, InterfaceSizeMustBe

from ..motor import InterfaceGPIO, InterfacePWM

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class MotorDC
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class MotorDC(MotorBase):
    """
    MotorDC is an object designed to control DC motors and its operation depends
    on the chosen mode when the object is created.

    The operating modes are as follows:

    GPIO_SIMPLE: This is the most basic mode and only allows us to start and stop
    the engine. To function, we need a InterfaceGPIO with a single output channel.

    GPIO_REVERSIBLE: Besides to starting and stopping the motor, it allows us to
    reverse the direction of rotation. On the electronic level needs a H-bridge
    for controlling the motor and an InterfaceGPIO with two output channels.

    PWM_SIMPLE: It works exactly like the GPIO SIMPLE mode but with the ability to
    control the speed. For this you need an InterfacePWM with one output channel.

    PWM_REVERSIBLE: In this mode besides controlling the rotational speed, allows
    change the direction. Requires an InterfacePWM with two output channels. Like the
    GPIO_REVERSIBLE mode, we need an H-bridge to control the motor.

    ADV_REVERSIBLE: This mode is intended to control dc motors through integrated
    circuit like the L298N, L293D, DRV8833 or similars. It need to receive a tuple with
    an InterfaceGPIO object with two channels and an InterfacePWM object. The channels
    of the InterfaceGPIO will control the power transistors that determine the direction
    of the rotation and the InterfacePWM will control the output inhibitor of these
    transistors, thereby we can control the speed and direction of rotation.
    """

    GPIO_SIMPLE, \
    GPIO_REVERSIBLE, \
    PWM_SIMPLE, \
    PWM_REVERSIBLE, \
    ADV_REVERSIBLE = range(5)

    def __init__(self, iface, mode=0, frequency=100, dutycycle=100, name=None, start=None, stop=None):

        if not mode or mode in (self.GPIO_SIMPLE, self.GPIO_REVERSIBLE):
            if not isinstance(iface, InterfaceGPIO):
                raise InterfaceTypeMustBe('GPIO mode' , 'InterfaceGPIO')

            if mode == self.GPIO_SIMPLE and len(iface) < 1:
                raise InterfaceSizeMustBe(iface.__class__, 1)

            elif mode == self.GPIO_REVERSIBLE and len(iface) < 2:
                raise InterfaceSizeMustBe(iface.__class__, 2)

        elif mode in (self.PWM_SIMPLE, self.PWM_REVERSIBLE):
            if not isinstance(iface, InterfacePWM):
                raise InterfaceTypeMustBe('PWM mode' , 'InterfacePWM')

            if mode == self.PWM_SIMPLE and len(iface) < 1:
                raise InterfaceSizeMustBe(iface.__class__, 1)

            elif mode == self.PWM_REVERSIBLE and len(iface) < 2:
                raise InterfaceSizeMustBe(iface.__class__, 2)

        elif mode == self.ADV_REVERSIBLE:
            ifpwm = filter(lambda x: isinstance(x, InterfacePWM), iface)[0]
            ifdir = filter(lambda x: isinstance(x, InterfaceGPIO), iface)[0]

            if not ifpwm or not ifdir:
                raise Exception('The ADV_REVERSIBLE mode need a tuple with an InterfaceGPIO and an InterfacePWM as interfaces')

            if len(ifdir) < 2:
                raise InterfaceSizeMustBe(ifdir.__class__, 2)

            iface = ifdir, ifpwm

        else:
            raise Exception('Unknown work mode for MotorDC class')

        super(MotorDC, self).__init__(iface, name, start, stop)

        self._mode = mode
        self._direction = None
        self._frequency = 50
        self._dutycycle = 100
        self._pwm_enabled = mode in (self.PWM_SIMPLE, self.PWM_REVERSIBLE, self.ADV_REVERSIBLE)

        self._worker = Worker(self.__run__)

        self.set_frequency(frequency)
        self.set_dutycycle(dutycycle)


    def __run__(self, moveto, timeout):
        self.action_start()

        if self._mode == self.GPIO_SIMPLE:
            self.__write_gpio__(0x01)

        elif self._mode == self.GPIO_REVERSIBLE:
            self.__write_gpio__(0x01 if moveto == self.MOVE_RIGHT else 0x02)

        elif self._mode == self.PWM_SIMPLE:
            self.__write_pwm__(0, self._dutycycle)

        elif self._mode == self.PWM_REVERSIBLE:
            self.__write_pwm__(0, self._dutycycle if moveto == self.MOVE_RIGHT else 0)
            self.__write_pwm__(1, self._dutycycle if moveto == self.MOVE_LEFT else 0)

        elif self._mode == self.ADV_REVERSIBLE:
            self.__write_pwm__(0, self._dutycycle)
            self.__write_gpio__(0x01 if moveto == self.MOVE_RIGHT else 0x02)

        if not timeout:
            self._worker.wait()

        else:
            self._worker.wait(timeout)
            self.stop()

        self.action_stop()


    def __write_pwm__(self, channel, dutycycle):
        if not isinstance(self._iface, tuple):
            self._iface.write(channel, dutycycle)
        else:
            self._iface[1].write(channel, dutycycle)


    def __write_gpio__(self, data):
        if not isinstance(self._iface, tuple):
            self._iface.write(data)
        else:
            self._iface[0].write(data)


    def set_dutycycle(self, pulse):
        """  """

        if not self._pwm_enabled:
            return

        if pulse is None:
            return

        if not isinstance(pulse, (int, long, float)):
            raise InvalidTypeError('The dutycycle', 'numeric')

        if pulse != self._dutycycle:
            self._dutycycle = pulse


    def set_frequency(self, freq):
        """  """

        if not self._pwm_enabled:
            return

        if not isinstance(freq, (int, long, float)):
            raise InvalidTypeError('The frequency', 'numeric')

        if freq != self._frequency:
            self._frequency = freq


    def get_dutycycle(self):
        """  """
        return self._dutycycle


    def get_direction(self):
        """  """
        return self._direction


    def alive(self):
        """  """
        return self._worker.alive()


    def speed_up(self, value=1):
        """ Increase the speed, this method only works with modes that an InterfacePWM was defined """

        if not self._pwm_enabled or not self.alive():
            return

        if not isinstance(value, (int, long, float)):
            raise InvalidTypeError('The speed value', 'numeric')

        if self._dutycycle >= 100:
            return

        self._dutycycle = self._dutycycle + value if (self._dutycycle + value) < 100 else 100
        self.__write_pwm__(0, self._dutycycle)


    def speed_down(self, value=1):
        """ Decrease the speed, this method only works with modes that an InterfacePWM was defined """

        if not self._pwm_enabled or not self.alive():
            return

        if not isinstance(value, (int, long, float)):
            raise InvalidTypeError('The speed value', 'numeric')

        if self._dutycycle <= 0:
            return

        self._dutycycle = self._dutycycle - value if (self._dutycycle - value) > 0 else 0
        self.__write_pwm__(0, self._dutycycle)


    def stop(self):
        """ Stops the motor """

        if self._worker.alive():
            self._worker.stop()

            if not self._pwm_enabled:
                self._iface.write(0)

            else:
                if not isinstance(self._iface, tuple):
                    self._iface.write(0, 0)
                    self._iface.write(1, 0)

                else:
                    self._iface[0].write(0)
                    self._iface[1].write(0, 0)


    def forward(self, dutycycle=None, timeout=None):
        """ Move the motor to the right """

        self.set_dutycycle(dutycycle)
        self._worker.start(args=(self.MOVE_RIGHT, timeout))


    def backward(self, dutycycle=None, timeout=None):
        """ Move the motor to the left """

        if self._mode in (self.GPIO_SIMPLE, self.PWM_SIMPLE):
            return

        self.set_dutycycle(dutycycle)
        self._worker.start(args=(self.MOVE_LEFT, timeout))
