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

from initlogging import logging
from aridimpl.model import Function, Number
from system import screen
from screen import screenenv
from termios import TIOCGWINSZ
from pathlib import Path
import tempfile, sys, aridity, shutil, struct, fcntl, os, argparse

log = logging.getLogger(__name__)

def toabswidth(context, resolvable):
    winsize = 'HHHH'
    ws_col = struct.unpack(winsize, fcntl.ioctl(sys.stdin, TIOCGWINSZ, bytes(struct.calcsize(winsize))))[1]
    return Number(round(resolvable.resolve(context).value * (ws_col - 1))) # Take off 1 for the separator.

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chdir', type = os.path.expanduser)
    config, vimargs = parser.parse_known_args()
    if config.chdir is not None:
        os.chdir(config.chdir)
    configdir = Path.home() / '.Concern'
    configdir.mkdir(parents = True, exist_ok = True)
    with tempfile.TemporaryDirectory(dir = str(configdir)) as tempdir:
        projectdir = Path(__file__).resolve().parent
        tempdir = Path(tempdir)
        concernvimrc = tempdir / 'vimrc'
        sendblock = tempdir / 'sendblock.py'
        screenrc = tempdir / 'screenrc'
        context = aridity.Context()
        context['Concern', 'toAbsWidth'] = Function(toabswidth)
        with aridity.Repl(context) as repl:
            printf = repl.printf
            printf("cd %s", projectdir)
            printf('. Concern.arid')
            settings = Path.home() / '.settings.arid'
            if settings.exists():
                printf(". %s", settings)
            else:
                log.info("No such file: %s", settings)
            uservimrc = Path.home() / '.vimrc'
            if uservimrc.exists():
                printf("vimrc userPath = %s", uservimrc)
            else:
                log.info("No such file: %s", uservimrc)
            printf('Concern')
            printf("\tinterpreter = %s", sys.executable)
            printf("\tvimrcPath = %s", concernvimrc)
            printf("\tsendblock = %s", sendblock)
            if vimargs:
                printf('\tvimArgs := $list()')
                for arg in vimargs:
                    printf("\tvimArgs += %s", arg)
            printf("redirect %s", concernvimrc)
            printf('Concern < vimrc.aridt')
            printf('" = $(pystr)')
            printf("redirect %s", sendblock)
            printf('Concern < sendblock.py.aridt')
            printf('" = $(screenstr)')
            printf("redirect %s", screenrc)
            printf('Concern < screenrc.aridt')
        for path in tempdir / 'getblock.py',:
            shutil.copy2(str(projectdir / path.name), str(path))
        doublequotekey = context.resolved('Concern', 'doubleQuoteKey').value
        screen('-S', context.resolved('Concern', 'sessionName').value, '-c', str(screenrc), env = screenenv(doublequotekey))

if '__main__' == __name__:
    main()
