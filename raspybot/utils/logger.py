#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
# Name:         logger
# Purpose:
#
# Author:       Bentejuy Lopez
# Created:      02/19/2016
# Modified:     03/27/2016
# Version:      0.0.07
# Copyright:    (c) 2016 Bentejuy Lopez
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

import sys
import logging

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger()
logger.setLevel(logging.DEBUG if __debug__ else logging.WARNING)

if not logger.handlers:
    hld = logging.StreamHandler(sys.stdout)
    hld.setLevel(logging.DEBUG if __debug__ else logging.WARNING)
    hld.setFormatter(logging.Formatter('%(levelname)s :: %(name)s [%(lineno)d] => %(message)s'))

    logger.addHandler(hld)
