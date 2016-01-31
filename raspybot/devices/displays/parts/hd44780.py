#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         hd44780
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      12/28/2015
# Modified:     01/31/2016
# Version:      0.0.67
# Copyright:
# Licence:      GLPv3
#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from time import sleep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class HD44780
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class HD44780(object):

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
        self._light = 0x08
        self._blink = 0x01
        self._cursor = 0x02

        #  Command sequences for initialization (HD44780.pdf - Figures 23 and 24)
        self.__write__(*self.__command__(self.SET_DATA_8))
        self.__write__(*self.__command__(self.SET_DATA_8))
        self.__write__(*self.__command__(self.SET_DATA_8 if self._double else self.SET_DATA_4))
        self.__write__(*self.__command__(self.TURN_OFF))
        self.__write__(*self.__command__(self.CLEAR_DISPLAY))
        self.__write__(*self.__command__(self.ENTRY_MODE))


    def __command__(self, cmd):

        """
        Information taken from official datasheet: https://www.sparkfun.com/datasheets/LCD/HD44780.pdf

        D7  D6  D5  D4  D3  D2  D1  D0  EN  RW  RS
        |   |   |   |   |   |   |   |   |   |   |
        0   0   1   DL  N   F   0   0   0   0   0   ->   Funcion set, DL=1 => 8 bit bus data, N=1 => 2 lines, F=0 => 5x8 dots
        |   |   |   |   |   |   |   |   |   |
        0   0   1   1   *   *   *   *   0   0   0   ->   Funcion set (Interface to 8 bits), 4.1 ms
        |   |   |   |   |   |   |   |   |   |
        0   0   1   0   *   *   *   *   0   0   0   ->   Funcion set (Interface to 4 bits), 4.1 ms
        |   |   |   |   |   |   |   |   |   |
        0   0   0   0   0   0   0   1   0   0   0  ->   Clear Display,
        |   |   |   |   |   |   |   |   |   |
        0   0   0   0   0   1  I/D  S   0   0   0  ->   Entry mode set. I/D=1 => increment cursor, S=1 => display shift with cursor
        |   |   |   |   |   |   |   |   |   |
        0   0   0   0   0   0   1   0   0   0   0  ->   Go Home, 1.52 ms
        |   |   |   |   |   |   |   |   |   |
        0   0   0   0   0   0   0   1   0   0   0   ->   Clear display

        """


        if cmd == self.GO_HOME:
            return 0x02, 0x0,  0.005                 # 0b000000100 = 0x02

        elif cmd == self.ENTRY_MODE:
            return 0x28, 0x0, 0.0002                 # 0b001010000 = 0x28

        elif cmd == self.TURN_ON:
            return 0x0C | self._cursor | self._blink, 0x0, 0.0002      # 0b00001100 = 0x0C

        elif cmd == self.TURN_OFF:
            return 0x08 | self._cursor | self._blink, 0x0, 0.0002      # 0b00001000 = 0x08

        elif cmd == self.SET_DATA_4:
            return 0x32, 0x0, 0.0002                #   0b001100100 = 0x32

        elif cmd == self.SET_DATA_8:
            return 0x3A, 0x0, 0.0002                #   0b001110100 = 0x3A

        elif cmd == self.CLEAR_DISPLAY:
            return 0x01, 0x0, 0.005                 #   0b000000001 = 0x01

        elif cmd == self.CURSOR_TO:
            return 0x80, 0x0, 0.0002                #   0b100000000 = 0x80

        elif cmd == self.CURSOR_LEFT:
            return 0x10, 0x0, 0.0002                #   0b000100000 = 0x10

        elif cmd == self.CURSOR_RIGHT:
            return 0x14, 0x0, 0.0002                #   0b000101000 = 0x14


    def __enable_data_i2c__(self, data):
        sleep(0.0005)
        self._iface.write_byte(data | 0x04 | self._light)
        sleep(0.0005)
        self._iface.write_byte(data & 0xF3 | self._light)


    def __enable_data_gpio__(self, data):
        if self._double:
            sleep(0.0005)
            self._iface.write_quick(data | 0x004)
            sleep(0.0005)
            self._iface.write_quick(data & 0x7FB)

        else:
            sleep(0.0005)
            self._iface.write_quick(data | 0x04)
            sleep(0.0005)
            self._iface.write_quick(data & 0x7B)


    def __write__(self, data, flags, timeout):
        pass


    def __write_gpio__(self, data, flags, timeout):
        if self._double:
            data = data << 3 | flags

            self._iface.write_quick(data)
            self.__enable_data_gpio_(data)
            sleep(timeout)

        else:
            lbits = (data & 0x0F) << 3 | flags
            hbits = (data & 0xF0) >> 1 | flags

            self._iface.write_quick(hbits)
            self.__enable_data_gpio__(hbits)
            sleep(timeout)

            self._iface.write_quick(lbits)
            self.__enable_data_gpio__(lbits)
            sleep(timeout)


    def __write_i2c__(self, data, flags, timeout):
        hbits = (data & 0xF0 ) | (flags | self._light)
        lbits = (data & 0x0F) << 4 | (flags | self._light)

        self._iface.write_byte(hbits)
        self.__enable_data_i2c__(hbits)
        sleep(timeout)

        self._iface.write_byte(lbits)
        self.__enable_data_i2c__(lbits)
        sleep(timeout)


    def __row_offset__(self, col, row):
        col = 0 if col >= self._cols else col
        row = 0 if row >= self._rows else self._offsets[row]

        return row + col


    def on(self):
        self.__write__(*self.__command__(self.TURN_ON))


    def off(self):
        self.__write__(*self.__command__(self.TURN_OFF))


    def clear(self):
        self.__write__(*self.__command__(self.CLEAR_DISPLAY))


    def home(self):
        self.__write__(*self.__command__(self.GO_HOME))


    def goto(self, col, row):
        cmd, flags, timeout = self.__command__(self.CURSOR_TO)
        cmd |= self.__row_offset__(col, row)

        self.__write__(cmd, flags, timeout)


    def write(self, char, col=None, row=None):
        if not None in (col, row):
            self.goto(col, row)

        self.__write__(ord(char), 0x01, 0.0005)


    def writeln(self, text):
        for char in text:
            if char == '\n':
                self.__write__(0xC0, 0, 0.0005)
            else:
                self.__write__(ord(char), 0x01, 0.0005)


    def set_cursor(self, enable, blink=True):
        self._blink = 0x01 if enable else 0
        self._cursor = 0x02 if blink else 0

        self.__write__(*self.__command__(self.TURN_ON))


    def set_backlight(self, on):
        self._light = 0x08 if on else 0

        self.__write__(*self.__command__(self.TURN_ON))
