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

from concernlib.initlogging import logging
from aridimpl.model import Function, Number
from lagoon import screen
from screen import screenenv
from termios import TIOCGWINSZ
from pathlib import Path
from pkg_resources import resource_filename
import tempfile, sys, aridity, shutil, struct, fcntl, os, argparse, importlib

log = logging.getLogger(__name__)

def toabswidth(context, resolvable):
    winsize = 'HHHH'
    ws_col = struct.unpack(winsize, fcntl.ioctl(sys.stdin, TIOCGWINSZ, bytes(struct.calcsize(winsize))))[1]
    return Number(round(resolvable.resolve(context).value * (ws_col - 1))) # Take off 1 for the separator.

def main_Concern():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chdir', type = os.path.expanduser)
    config, vimargs = parser.parse_known_args()
    if config.chdir is not None:
        os.chdir(config.chdir)
    configdir = Path.home() / '.Concern'
    configdir.mkdir(parents = True, exist_ok = True)
    with tempfile.TemporaryDirectory(dir = str(configdir)) as tempdir:
        tempdir = Path(tempdir)
        concernvimrc = tempdir / 'vimrc'
        sendblock = tempdir / 'sendblock.py'
        quit = tempdir / 'quit.py'
        screenrc = tempdir / 'screenrc'
        context = aridity.Context()
        context['Concern', 'toAbsWidth'] = Function(toabswidth)
        with aridity.Repl(context) as repl:
            printf = repl.printf
            printf(". %s", resource_filename('concernlib', 'Concern.arid'))
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
            printf("\tquit = %s", quit)
            printf('\tvimArgs := $list()')
            for arg in vimargs:
                printf("\tvimArgs += %s", arg)
        importlib.import_module("concernlib.%s" % context.resolved('Concern', 'consumerName').value).configure(context)
        with aridity.Repl(context) as repl:
            printf = repl.printf
            printf("redirect %s", concernvimrc)
            printf("Concern < %s", resource_filename('concernlib', 'vimrc.aridt'))
            printf('" = $(pystr)')
            printf("redirect %s", sendblock)
            printf("Concern < %s", resource_filename('concernlib', 'sendblock.py.aridt'))
            printf("redirect %s", quit)
            printf("Concern < %s", resource_filename('concernlib', 'quit.py.aridt'))
            printf('" = $(screenstr)')
            printf("redirect %s", screenrc)
            printf("Concern < %s", resource_filename('concernlib', 'screenrc.aridt'))
        for path in tempdir / 'getblock.py',:
            shutil.copy2(resource_filename('concernlib', path.name), str(path))
        doublequotekey = context.resolved('Concern', 'doubleQuoteKey').value
        screen.print('-S', context.resolved('Concern', 'sessionName').value, '-c', screenrc, env = screenenv(doublequotekey))
