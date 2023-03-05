# Copyright 2019, 2021, 2022 Andrzej Cichocki

# This file is part of Concern.
#
# Concern is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Concern is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Concern.  If not, see <http://www.gnu.org/licenses/>.

from aridity.model import Number, Text
from struct import Struct
from termios import TIOCGWINSZ
import fcntl, logging, sys

winsize = Struct('HHHH')

def initlogging():
    logging.basicConfig(format = "%(asctime)s %(levelname)s %(message)s", level = logging.DEBUG)

def toabswidth(scope, resolvable):
    ws_col = winsize.unpack(fcntl.ioctl(sys.stdin, TIOCGWINSZ, bytes(winsize.size)))[1]
    return Number(round(resolvable.resolve(scope).scalar * (ws_col - 1))) # Take off 1 for the separator.

def vimstr(scope, resolvable):
    return Text(f"""'{resolvable.resolve(scope).cat().replace("'", "''")}'""")
