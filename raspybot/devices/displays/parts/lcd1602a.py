#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         LCD1602A
# Purpose:      Specific object to control LCD 1602A with GPIO connection
#
# Author:       Bentejuy Lopez
# Created:      12/28/2015
# Modified:     01/05/2016
# Version:      0.0.43
# Copyright:
# Licence:      GLPv3
#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class LCD1602AD
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class LCD1602AD:

    GO_HOME, \
    TURN_ON,\
    TURN_OFF,\
    SET_DATA_4, \
    SET_DATA_8, \
    CURSOR_TO, \
    ENTRY_MODE, \
    CURSOR_LEFT, \
    CURSOR_RIGHT, \
    CLEAR_DISPLAY = range(10)


    def __init__(self, iface):

        self._iface = iface
        self._blink = True
        self._cursor = True
        self._double = len(iface) >= 10

        #  Command sequences for initialization (HD44780.pdf - Figures 23 and 24)

        self.__write__(*self.__command__(self.SET_DATA_8))
        self.__write__(*self.__command__(self.SET_DATA_8))
        self.__write__(*self.__command__(self.SET_DATA_8 if self._double else self.SET_DATA_4))
        self.__write__(*self.__command__(self.TURN_OFF))
        self.__write__(*self.__command__(self.CLEAR_DISPLAY))
        self.__write__(*self.__command__(self.ENTRY_MODE))


    def __enable_data__(self, data):
        if self._double:
            time.sleep(0.005)
            self._iface.write_quick(data | 0x002)
            time.sleep(0.005)
            self._iface.write_quick(data & 0x3FD)
            time.sleep(0.005)

        else:
            time.sleep(0.0005)
            self._iface.write_quick(data | 0x02)
            time.sleep(0.0005)
            self._iface.write_quick(data & 0x3D)


    def __write__(self, data, timeout):
        if self._double:
            self._iface.write_quick(data)
            self.__enable_data__(data)
            time.sleep(timeout)

        else:
            lbits = data & 0x3F
            hbits = data & 0x03 | (data >> 4 & 0x3C)

            self._iface.write_quick(hbits)
            self.__enable_data__(hbits)
            time.sleep(timeout)

            self._iface.write_quick(lbits)
            self.__enable_data__(lbits)
            time.sleep(timeout)



    def __command__(self, cmd):

        """
        Information taken from official datasheet: https://www.sparkfun.com/datasheets/LCD/HD44780.pdf

        D7  D6  D5  D4  D3  D2  D1  D0  E  RS
        |   |   |   |   |   |   |   |   |   |
        0   0   1   DL  N   F   0   0   0   0   ->   Funcion set, DL=1 => 8 bit bus data, N=1 => 2 lines, F=0 => 5x8 dots
        |   |   |   |   |   |   |   |   |   |
        0   0   1   1   *   *   *   *   0   0   ->   Funcion set (Interface to 8 bits), 4.1 ms
        |   |   |   |   |   |   |   |   |   |
        0   0   1   0   *   *   *   *   0   0   ->   Funcion set (Interface to 4 bits), 4.1 ms
        |   |   |   |   |   |   |   |   |   |
        0   0   0   0   0   0   0   1   0   0   ->   Clear Display,
        |   |   |   |   |   |   |   |   |   |
        0   0   0   0   0   1  I/D  S   0   0   ->   Entry mode set. I/D=1 => increment cursor, S=1 => display shift with cursor
        |   |   |   |   |   |   |   |   |   |
        0   0   0   0   0   0   1   0   0   0   ->   Go Home, 1.52 ms
        |   |   |   |   |   |   |   |   |   |
        0   0   0   0   0   0   0   1   0   0   ->   Clear display

        """


        if cmd == self.GO_HOME:
            return 0x008, 0.005                 # 0b0000001000 = 0x02 << 2

        elif cmd == self.ENTRY_MODE:
            return 0x0A0, 0.0002                # 0b0010100000 = 0x28 << 2

        elif cmd == self.TURN_ON:
            return 0x030 | (0x1 << 3 if self._cursor else 0) | (0x1 << 2 if self._blink else 0), 0.0002      # 0b0000110000 = 0x0C << 2

        elif cmd == self.TURN_OFF:
            return 0x020 | (0x1 << 3 if self._cursor else 0) | (0x1 << 2 if self._blink else 0), 0.0002      # 0b0000100000 = 0x08 << 2

        elif cmd == self.SET_DATA_4:
            return 0x0C8, 0.0002                #   0b0011001000 = 0x32 << 2

        elif cmd == self.SET_DATA_8:
            return 0x0E8, 0.0002                #   0b0011101000 = 0x3A << 2

        elif cmd == self.CLEAR_DISPLAY:
            return 0x004, 0.005                 #   0b0000000100 = 0x01 << 2

        elif cmd == self.CURSOR_TO:
            return 0x200, 0.0002                #   0b1000000000 = 0x80 << 2

        elif cmd == self.CURSOR_LEFT:
            return 0x040, 0.0002                #   0b0001000000 = 0x10 << 2

        elif cmd == self.CURSOR_RIGHT:
            return 0x050, 0.0002                #   0b0001010000 = 0x14 << 2


    def on(self):
        """  """
        self.__write__(*self.__command__(self.TURN_ON))


    def off(self):
        """  """
        self.__write__(*self.__command__(self.TURN_OFF))


    def clear(self):
        """  """
        self.__write__(*self.__command__(self.CLEAR_DISPLAY))


    def home(self):
        """  """
        self.__write__(*self.__command__(self.GO_HOME))


    def goto(self, x, y):
        """  """

        x = 0x27 if x > 0x27 else x
        y = 0x40 if y > 0x00 else 0

        cmd, timeout = self.__command__(self.CURSOR_TO)
        cmd |= ((x + y) << 2)

        self.__write__(cmd, timeout)


    def write(self, char, x=None, y=None):
        """  """

        if not x is None and not y is None:
            self.goto(x, y)

        self.__write__(ord(char) << 2 | 0x01, 0.0005)


    def writeln(self, text):
        """  """

        for char in text:
            self.__write__(0x300 if char == '\n' else ord(char) << 2 | 0x01, 0.0005)


    def set_cursor(self, enable, blink=True):
        """  """

        self._blink = blink
        self._cursor = enable

        self.__write__(*self.__command__(self.TURN_ON))
