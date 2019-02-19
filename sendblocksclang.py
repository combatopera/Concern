# Copyright 2019 Andrzej Cichocki

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

from getblock import readblock, pilcrow, eol
from pym2149 import osctrl
from stufftext import stuff
import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # XXX: Close it?
    sock.sendto(osctrl.Message('/foxdot', [readblock('')]).ser(), ('localhost', 57120))
    text, _ = sock.recvfrom(1024)
    stuff(eol.join(text.decode('utf_8').splitlines()) + pilcrow + eol)

if '__main__' == __name__:
    main()
