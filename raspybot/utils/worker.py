#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         worker
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      04/17/2013
# Modified:     01/04/2015
# Version:      0.1.95
# Copyright:    (c) 2013-2015 Bentejuy Lopez
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

import Queue
import logging
import threading

from tasks import Task
from exceptions import InvalidFunctionError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class Worker
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class Worker(object):
    def __init__(self, runner):
        if not hasattr(runner, '__call__'):
            raise InvalidFunctionError('runner')

        self._event  = threading.Event()
        self._runner = runner
        self._thread = None


    def __start__(self, args):
        if self.alive():
            self.__stop__()

        self._event.clear()
        self._thread = threading.Thread(target=self._runner, args=args)
        self._thread.setDaemon(True)
        self._thread.start()


    def __stop__(self):
        self._event.set()

        try:
            if self.alive():
                self._thread.join(.1)

        except:
            pass

        finally:
            self._thread = None


    def set(self):
        """  """
        self._event.set()


    def clear(self):
        """  """
        self._event.clear()


    def wait(self, delay=None):
        """  """
        return self._event.wait(delay)


    def is_set(self):
        """  """
        return self._event.is_set()


    def alive(self):
        """  """
        return self._thread and self._thread.is_alive()


    def join(self, timeout=None):
        """  """

        if self._thread:
            self._thread.join(timeout)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Class WorkerTask
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class WorkerTask(Worker):
    def __init__(self, parser, delay, checker=None):
        super(WorkerTask, self).__init__(self.__run__)

        if not hasattr(parser, '__call__'):
            raise InvalidFunctionError('parser')

        if checker and not hasattr(checker, '__call__'):
            raise InvalidFunctionError('checker')

        self._delay = delay
        self._lock  = threading.Lock()
        self._queue = Queue.Queue()

        self._parser  = parser
        self._checker = checker


    def __start__(self):
        super(WorkerTask, self).__start__(())


    def __stop__(self):
        super(WorkerTask, self).__stop__()

        try:
            self._lock.acquire()

            while not self._queue.empty():
                self._queue.get_nowait()
                self._queue.task_done()

        finally:
            self._lock.release()


    def __run__(self):
        task = None
        delay = 0

        while not self._event.is_set():
            if task:
                delay = self._parser(task)

                if delay:
                    self._event.wait(delay)

                else:
                    task = None

            else:
                if self._queue.empty():
                    task = self._queue.get(True)
                    self._queue.task_done()

                else:
                    self._lock.acquire()
                    task = self._queue.get()
                    self._lock.release()

                    self._event.wait(self._delay)


    def __append__(self, *tasks):
        try:
            self._lock.acquire()

            for task in tasks:
                self._queue.put(task)

        except Exception as error:
            logger.critical(error)

        finally:
            self._lock.release()


    def empty(self):
        """  """
        return self._queue.empty()
