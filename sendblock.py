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
import socket, sys

def sclang():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # XXX: Close it?
    # FIXME: This must not send a message bigger than pym2149 bufsize.
    sock.sendto(osctrl.Message('/foxdot', [readblock('')]).ser(), ('localhost', 57120))
    sock.settimeout(5) # Give up eventually, if pym2149 has a problem.
    text, _ = sock.recvfrom(1024) # XXX: Big enough for any pym2149 response?
    stuff(eol.join(text.decode('utf_8').splitlines()) + pilcrow + eol)

def foxdot():
    stuff(readblock())

dispatch = {
    (1, 'default'): sclang,
    (1, 'alternate'): foxdot,
    (2, 'default'): foxdot,
    (2, 'alternate'): sclang,
}

def main():
    s = slice(1, 3)
    window, target = sys.argv[s]
    del sys.argv[s]
    dispatch[int(window), target]()

if '__main__' == __name__:
    main()
