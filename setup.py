"""
Copyright (c) 2015 Bentejuy Lopez

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import os
import sys
import glob

from distutils.core import setup

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def find_packages(path, excludes=None):
    paths = []

    for root, subdirs, files in os.walk(path):
        if excludes and root in excludes:
            continue

        for f in files:
            if f.rfind('.py') > 0:
                paths.append(root)
                break

    return paths

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

setup(
    name = "raspybot",
    packages = find_packages('raspybot'),
    version = "0.1.9",
    description = "Multipurpose library oriented to the Raspberry Pi.",
    author = "Bentejuy Lopez",
    author_email = "bentejuy@gmail.com",
    url = "http://raspybot.com",
    download_url = "http://raspybot.com/download.html",
    keywords = ["Raspberry Pi", "GPIO"],
    classifiers = [
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 1 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: End Users",
        "Intended Audience :: Developers",
        "License :: GNU GPLv3",
        "Topic :: Software Development :: Libraries :: Raspberry Pi",
    ],
    long_description = open('README.txt').read() + open('CHANGELOG.txt').read()
)
