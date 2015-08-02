#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         Motor
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      01/07/2015
# Modified:     07/28/2015
# Version:      0.0.75
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

from device import ActionDevice

from ..utils.worker import Worker
from ..utils.timeit import timeit
from ..utils.exceptions import InvalidTypeError, UnknowMotorModeError, IsRunningError, OutRangeError, InvalidRangeError, MinMaxValueError,InterfaceNoSupported

from ..io.interface import InterfacePWM
from ..io.interface import InterfaceGPIO

from motors.motorbase import MotorBase
from motors.motorservo import MotorServo
from motors.motorstepper import MotorStepper
from motors.motorstepperbipolar import MotorStepperBipolar
from motors.motorstepperunipolar import MotorStepperUnipolar

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
