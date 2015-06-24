#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         tests/flipflop.py
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      04/07/2015
# Modified:     05/28/2015
# Version:      0.0.43
# Copyright:    (c) 2015 Bentejuy Lopez
# Licence:      MIT
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import sys
import time
import math
import array
import random
import logging

import wave
import pygame

from tempfile import mkdtemp
from collections import deque
from Queue import Queue as queue, Empty as EmptyException

from raspybot.devices.logic import Blinker
from raspybot.devices.button import Buttons
from raspybot.io.interface import InterfaceManager, InterfaceGPIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def logger_init(debug=None):
    log = logging.getLogger('')

    hld = logging.StreamHandler(sys.stdout)
    hld.setLevel(debug and logging.DEBUG or logging.WARNING)
    hld.setFormatter(logging.Formatter('%(levelname)s :: %(name)s [%(lineno)d] --> %(message)s'))
    log.addHandler(hld)

    log.setLevel(debug and logging.DEBUG or logging.WARNING)

    return log

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logger_init(True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
#   Class SoundSystem
#
#   Note:
#       Some portions of code to generate the sounds were taken from this web pages,
#       Unfortunately I don't know his license.
#
#       https://zach.se/generate-audio-with-python/
#       http://code.activestate.com/recipes/578168-sound-generator-using-wav-file/
#       http://soledadpenades.com/2009/10/29/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class SoundSystem(object):

    #  Notes: http://www.phy.mtu.edu/~suits/notefreqs.html
    NOTES = {
        'red':    440.00,   #A4
        'blue':   587.33,   #D5
        'green':  698.46,   #F5
        'yellow': 880.00,   #A5
        'error':  220.00,   #A3
        'start':  987.77    #B5
    }

    CHANNELS = 1
    SAMPLERATE = 44100

    def __init__(self):

        pygame.display.init()

        pygame.mixer.pre_init(self.SAMPLERATE, -16, 1, 4096)
        pygame.mixer.init()

        self._sounds = {}
        self._channel = pygame.mixer.Channel(0)
        self._tmppath = mkdtemp(prefix=sys.argv[0])

        for name, note in self.NOTES.iteritems():
            fname = self.__file__(name)

            if self.__makefilewav__(fname, note, 1):
                self._sounds[name] = pygame.mixer.Sound(fname)


    def __del__(self):
        self.stop()
#       pygame.mixer.quit()

        try:
            for name in self.NOTES.keys():
                os.remove(self.__file__(name))

            os.rmdir(self._tmppath)

        except:
            pass


    def __file__(self, name):
        return os.path.join(self._tmppath, '{}.wav'.format(name))


    def __makefilewav__(self, fname, freq, duration=3, volume=100):
        data = array.array('h')
        size = int(self.SAMPLERATE * duration)

        if isinstance(freq, (int, long, float)):
            waves = self.SAMPLERATE / float(freq)

            for i in xrange(size):
                sample = 32767 * float(volume) / 100
                sample *= math.sin(math.pi * 2 * (i % waves / waves))
                data.append(int(sample))

        else:
            data.extend(random.sample(xrange(-32767, 32767), size))

        try:
            fwav = wave.open(fname, 'wb')

            fwav.setparams((self.CHANNELS, 2, self.SAMPLERATE, size, 'NONE', 'Uncompressed'))
            fwav.writeframes(data.tostring())
            fwav.close()

        except Exception, error:
            logger.error(error)

            return False

        return True


    def play(self, name):
        self.stop()

        try:
            self._channel.play(self._sounds[name])

        except Exception, error:
            logger.error(error)


    def stop(self):
        if self._channel.get_busy():
            self._channel.stop()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
#   Class SimonSays
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class SimonSays(object):

    LED_RED = 0b0100
    LED_BLUE = 0b0001
    LED_GREEN = 0b1000
    LED_YELLOW = 0b0010

    LEDS_ON  = 0b1111
    LEDS_OFF = 0b0000
    LEDS_LIST = (LED_BLUE, LED_YELLOW, LED_RED, LED_GREEN)

    SOUNDS = {
        LED_RED: 'red',
        LED_BLUE: 'blue',
        LED_GREEN: 'green',
        LED_YELLOW: 'yellow'
    }

    TIME_OUT = 10                                                   # Maximum time waiting for user response

    MODE_STOP, \
    MODE_START, \
    MODE_ERROR, \
    MODE_LOSER, \
    MODE_WINNER, \
    MODE_USER_TURN, \
    MODE_SIMON_TURN = range(7)


    def __init__(self, iface):

        self._index = 0                                             # Index of the deque readed
        self._level = 0
        self._action = self.MODE_STOP

        self._queue = queue()                                       # Object to store the sequence User's actions
        self._deque = deque()                                       # Object to store the sequence Simons's actions
        self._sounds = SoundSystem()
        self._blinker = Blinker(iface, 'blinker', delay=.1)
        self._buttons = Buttons(iface, 'buttons', release=self.on_response)

        # Defining all inputs channel on iface with the correct properties
        for btn in iface.get_in_ports():
            self._buttons.setup(btn, self._buttons.RELEASE, self._buttons.PUD_UP, 500)


    def on_response(self, obj, channel, action):
        """ Processes all user keystrokes """

        if self._action == self.MODE_USER_TURN:
            if channel == 4:
                pressed = self.LED_BLUE
            elif channel == 18:
                pressed = self.LED_RED
            elif channel == 17:
                pressed = self.LED_GREEN
            elif channel == 14:
                pressed = self.LED_YELLOW
            else:
                logger.error('Pressed the wrong button, probably bad configured')
                return

            self._queue.put(pressed)


    def stop_sound(self):
        self._sounds.stop()


    def start_sound(self, tone):
        try:
            if isinstance(tone, basestring):
                self._sounds.play(tone)
            else:
                self._sounds.play(self.SOUNDS[tone])

        except KeyError:
            logger.error('Index Sound {} not found.'.format(tone))


    def play_user(self, value, count):
        """   Execute sound/light when it process """

        self.start_sound(value)

        return value


    def play_game(self, value, count):
        """   Execute sound/light when to game stop """

        if count % 2:
            self.start_sound(value)
            value = 0

        else:
            self.stop_sound()
            value = self._deque[self._index]

            self._index += 1

        return value


    def play_stop(self, value, count):
        """ Execute sound/light when to game stop """

        self.start_sound(random.choice((self.LED_RED, self.LED_BLUE, self.LED_GREEN, self.LED_YELLOW)))

        return ~value


    def play_start(self, value, count):
        """ Execute sound/light when to game start """

        value = 1 << (count % 4)
        self.start_sound(value)

        return value


    def play_loser(self, value, count):
        """ Execute sound/light when the user lost the game """

        if not value:
            self.stop_sound()
        else:
            self.start_sound('error')

        return ~value


    def play_winner(self, value, count):
        """ Execute sound/light when the user won the game """

        self.start_sound(self.LED_GREEN)

        return ~value


    def next_step(self):
        """ Gets a new step and it makes some checks """

        leds = list(self.LEDS_LIST)

        if len(self._deque) > 3:
            last = self._deque[-1]

            # Check if the last 3 items are equals and remove if it is affirmative.
            if all(map(lambda x: x == last, list(self._deque)[-3:])):
                leds.remove(last)

        return random.choice(leds)


    def process(self, action, leds):
        """ Processes all actions """

        self._action = action

        try:
            self.stop_sound()
            self._blinker.stop()

            if action == self.MODE_STOP:
                logger.debug('Initializing the game in stop mode')
                """
                self._blinker.set_delay(.25)
                self._blinker.set_value(self.LED_RED)
                self._blinker.set_callback(self.play_stop)
                """
                self._blinker.set(0.25, self.LED_RED | self.LED_BLUE, self.play_stop)
                self._blinker.start(3.5)

            elif action == self.MODE_START:
                logger.debug('Initializing the game in start mode')
                self._blinker.set(.075, self.LED_RED, self.play_start)
                self._blinker.start(3)

            elif action == self.MODE_LOSER:
                logger.debug('Initializing the game in loser mode')
                self._blinker.set(1, self.LEDS_OFF, self.play_loser)
                self._blinker.start(6)

            elif action == self.MODE_WINNER:
                logger.debug('Initializing the game in winner mode')
                self._blinker.set(0.15, self.LEDS_OFF, self.play_winner)
                self._blinker.start(2.4)

            elif action == self.MODE_USER_TURN:
                logger.debug('Initializing the game in user turn')
                self._blinker.set(.75, leds, self.play_user)
                self._blinker.start(.75)

            elif action == self.MODE_SIMON_TURN:
                logger.debug('Initializing the game in Simon turn')
                time.sleep(1.5)

                self._blinker.set(round((10 - self._level) * 0.05, 1), leds, self.play_game)
                self._blinker.start()

            self._blinker.join()

        except KeyboardInterrupt:
            self._action = self.MODE_STOP

        finally:

            if action == self.MODE_STOP:
                pass

            elif action == self.MODE_START:
                self._index = 0
                self._action = self.MODE_SIMON_TURN

            elif action == self.MODE_LOSER:
                self._index = 0
                self._action = self.MODE_SIMON_TURN
                self._deque.clear()
                self._queue.task_done()

            elif action == self.MODE_WINNER:
                self._index = 0
                self._action = self.MODE_SIMON_TURN

            elif action == self.MODE_USER_TURN:
                if len(self._deque) > self._index + 1:
                    self._index += 1
                else:
                    # Each 5 hits, the difficulty level increases, because Simon increases his speed by 10%
                    if self._index and len(self._deque) % 5 == 0:

                        self._level += 1 if self._level < 9 else 0
                        self._action = self.MODE_WINNER
                    else:
                        self._index = 0
                        self._action = self.MODE_SIMON_TURN


            elif action == self.MODE_SIMON_TURN:
                self._index = 0
                self._action = self.MODE_USER_TURN

                # Emits sound message to begin user turn, Uncomment if you need help
                """
                self.start_sound('start')
                time.sleep(0.1)
                self.stop_sound()
                """


    def start(self):

        self.process(self.MODE_START, self.LEDS_ON)

        try:
            while True:
                if self._action == self.MODE_USER_TURN:
                    # Wait and proccess all events for user

                    if not self._queue.empty():
                        action = self._queue.get()
                    else:
                        try:
                            logger.debug('Waiting for user interaction....')
                            logger.debug('Buttons in Queue ({0}) => {1}'.format(len(self._deque), ' : '.join(map(str, self._deque))))

                            action = self._queue.get(True, self.TIME_OUT)

                        except EmptyException:
                            logger.info('Too much time waiting for user response, finished program.')
                            self.process(self.MODE_STOP, self.LEDS_OFF)

                            break


                    if action == self._deque[self._index]:
                        self.process(self.MODE_USER_TURN, action)

                    else:
                        self.process(self.MODE_LOSER, self.LEDS_OFF)


                elif self._action == self.MODE_SIMON_TURN:
                    # Generates and stores a new combination of sound/light
                    self._deque.append(self.next_step())

                    # Replay all the sounds/lights from the beginning
                    self.process(self.MODE_SIMON_TURN, self.LEDS_OFF)

                else:
                    # Proccess others actions.
                    self.process(self._action, self.LEDS_OFF)


        except KeyboardInterrupt:
            self.process(self.MODE_STOP, self.LEDS_ON)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

mgr = InterfaceManager()
ifg = InterfaceGPIO(mgr, pinin=(4, 14, 18, 17), pinout=(9, 25, 11, 8))


simon = SimonSays(ifg)
simon.start()
