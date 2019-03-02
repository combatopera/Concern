#!/usr/bin/env pyven

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

from aridimpl.model import Function, Number
from system import screen
from termios import TIOCGWINSZ
from pathlib import Path
import tempfile, sys, aridity, shutil, struct, fcntl

def toabswidth(context, resolvable):
    winsize = 'HHHH'
    ws_col = struct.unpack(winsize, fcntl.ioctl(sys.stdin, TIOCGWINSZ, bytes(struct.calcsize(winsize))))[1]
    return Number(round(resolvable.resolve(context).value * (ws_col - 1))) # Take off 1 for the separator.

def main():
    configdir = Path.home() / '.Concern'
    configdir.mkdir(parents = True, exist_ok = True)
    with tempfile.TemporaryDirectory(dir = configdir) as tempdir:
        projectdir = Path(__file__).resolve().parent
        tempdir = Path(tempdir)
        vimrc = tempdir / 'vimrc'
        sendblockfoxdot = tempdir / 'sendblockfoxdot.py'
        sendblocksclang = tempdir / 'sendblocksclang.py'
        screenrc = tempdir / 'screenrc'
        context = aridity.Context()
        context['Concern', 'toAbsWidth'] = Function(toabswidth)
        with aridity.Repl(context) as repl:
            printf = repl.printf
            printf("cd %s", projectdir)
            printf('. Concern.arid')
            printf('Concern')
            printf("\tinterpreter = %s", sys.executable)
            printf("\tvimrcPath = %s", vimrc)
            printf('\tsendblock')
            printf("\t\tfoxdot = %s", sendblockfoxdot)
            printf("\t\tsclang = %s", sendblocksclang)
            args = sys.argv[1:]
            if args:
                printf('\tvimArgs := $list()')
                for arg in args:
                    printf("\tvimArgs += %s", arg)
            printf("redirect %s", vimrc)
            printf('Concern < vimrc.aridt')
            printf('" = $(pystr)')
            printf("redirect %s", tempdir / 'stufftext.py')
            printf('Concern < stufftext.py.aridt')
            printf('" = $(screenstr)')
            printf("redirect %s", screenrc)
            printf('Concern < screenrc.aridt')
        for path in tempdir / 'getblock.py', sendblockfoxdot, sendblocksclang:
            shutil.copy2(projectdir / path.name, path)
        screen('-S', context.resolved('Concern', 'sessionName').value, '-c', screenrc)

if '__main__' == __name__:
    main()
