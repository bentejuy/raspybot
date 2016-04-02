#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         interfacepwm
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      07/22/2015
# Modified:     03/13/2016
# Version:      0.0.47
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

from ..interface import TaskPWM
from ..interface import InterfaceActive

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class InterfacePWM
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class InterfacePWM(InterfaceActive):
    """

    """

    def __init__(self, manager, pinout=None, frequency=50):
        super(InterfacePWM, self).__init__(manager, self.__parser__)

        self._pin = []
        self._pwm = []
        self._frequency = frequency

        if pinout:
            self.setup(pinout, frequency)


    def __len__(self):
       return len(self._pin)


    def __parser__(self, task):
        state = task.state

        if state == task.WAITING:
            if task.action == task.PWM_START:
                if state == task.WAITING:
                    self._pwm[task.index].start(task.dutycycle)

            elif task.action == task.PWM_STOP:
                self._pwm[task.index].stop()

        elif state == task.TIMEOUT or state == task.STOPPED:
                self._pwm[task.index].stop()

        return 0


    def __contains__(self, pin):
        return pin in self._pin


    def free(self):
        """  """

        self.stop()
        map(self._manager.cleanup, self._pin)

        self._pin = []
        self._pwm = []


    def setup(self, pin, frequency=50):
        """  """

        def append_in(pin):
            if pin in self._pin:
                return

            if len(self._pin) > 2:
                raise Exception('The InterfacePWM does not support more that two channels')

            self._manager.setup(pin, self._bus.HARD_PWM)

            self._pin.append(pin)
            self._pwm.append(None)


        if isinstance(pin, (tuple, list)):
            map(append_in, pin)

        else:
            append_in(pin)


    def stop(self, index=0):
        """  """

        super(self.__class__, self).stop()
        self.append(TaskPWM(TaskPWM.PWM_STOP, index=index))

        if not self.alive():
            super(self.__class__, self).start()


    def write(self, index, dutycycle, timeout=0):
        """ """

        if not self._pwm[index]:
            self._pwm[index] = self._bus.PWM(self._pin[index], self._frequency)

        self.append(TaskPWM(TaskPWM.PWM_START, dutycycle, index, timeout))

        if not self.alive():
            self.start()


    def set_frequency(self, freq):
        """  """
        self._frequency = freq
