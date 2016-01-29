#!/usr/bin/env python
# -+- coding: utf-8 -+-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         worker
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      04/17/2013
# Modified:     01/29/2016
# Version:      0.2.07
# Copyright:    (c) 2013-2016 Bentejuy Lopez
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
import threading

from .tasks import Task
from .exceptions import InvalidFunctionError

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


    def start(self, args):
        """ Start the worker."""

        if self.alive():
            self.stop()

        self._event.clear()
        self._thread = threading.Thread(target=self._runner, args=args)
        self._thread.setDaemon(True)
        self._thread.start()


    def stop(self):
        """ Stops the worker. """

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
        """ Checks if the Worker is alive. """
        return not self._thread is None and self._thread.is_alive()


    def join(self, timeout=None):
        """ Wait until the worker terminates or until the seconds defined in "timeout" has elapsed. """

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
    def __init__(self, parser, delay):
        super(WorkerTask, self).__init__(self.__run__)

        if not hasattr(parser, '__call__'):
            raise InvalidFunctionError('parser')

        self._delay = delay
        self._queue = Queue.Queue()

        self._parser  = parser


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
                    task = self._queue.get()
                    self._queue.task_done()

                else:
                    task = self._queue.get_nowait()

                    self._queue.task_done()
                    self._event.wait(self._delay)

    def start(self):
        """ Start the worker."""
        super(WorkerTask, self).start(())


    def stop(self):
        """ Stops the worker and clear all task pending. """

        super(WorkerTask, self).stop()

        while not self._queue.empty():
            self._queue.get_nowait()
            self._queue.task_done()


    def empty(self):
        """ Checks if the task queue is empty. """
        return self._queue.empty()


    def append(self, *tasks):
        """ Adds tasks to the worker. """

        for task in tasks:
            self._queue.put(task)

