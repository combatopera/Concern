# Copyright 2019, 2021 Andrzej Cichocki

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

from . import templates
from .initlogging import logging
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from aridity.model import Number
from aridity.util import openresource
from importlib import import_module
from pathlib import Path
from screen import stuffablescreen
from tempfile import TemporaryDirectory
from termios import TIOCGWINSZ
import fcntl, os, struct, sys

log = logging.getLogger(__name__)

def toabswidth(context, resolvable):
    winsize = 'HHHH'
    ws_col = struct.unpack(winsize, fcntl.ioctl(sys.stdin, TIOCGWINSZ, bytes(struct.calcsize(winsize))))[1]
    return Number(round(resolvable.resolve(context).scalar * (ws_col - 1))) # Take off 1 for the separator.

def _processtemplate(config, quotename, templatename, targetpath):
    child = (-config).childctrl()
    child.printf('" = $(%s)', quotename)
    with openresource(templates.__name__, templatename) as f:
        child.processtemplate(f, targetpath)

def main_Concern():
    'Vim-based live coding environment.'
    parser = ArgumentParser()
    parser.add_argument('--chdir', type = os.path.expanduser)
    config, vimargs = parser.parse_known_args()
    if config.chdir is not None:
        os.chdir(config.chdir)
    configdir = Path.home() / '.Concern'
    configdir.mkdir(parents = True, exist_ok = True)
    with TemporaryDirectory(dir = configdir) as tempdir:
        tempdir = Path(tempdir)
        concernvimrc = tempdir / 'vimrc'
        looppath = tempdir / 'loop.py'
        sendblock = tempdir / 'sendblock.py'
        quit = tempdir / 'quit.py'
        screenrc = tempdir / 'screenrc'
        ctrl = ConfigCtrl()
        ctrl.put('Concern', 'toAbsWidth', function = toabswidth)
        config = ctrl.loadappconfig(main_Concern, 'Concern.arid', settingsoptional = True)
        uservimrc = Path.home() / '.vimrc'
        if uservimrc.exists():
            (-config).printf("vimrc userPath = %s", uservimrc)
        else:
            log.info("No such file: %s", uservimrc)
        (-config).printf("vimrcPath = %s", concernvimrc)
        (-config).printf("looppath = %s", looppath)
        (-config).printf("sendblock = %s", sendblock)
        (-config).printf("quit = %s", quit)
        (-config).printf('vimArgs := $list()')
        for arg in vimargs:
            (-config).printf("vimArgs += %s", arg)
        (-config).printf("signalpath = %s", tempdir / 'signal')
        import_module(f".consumer.{config.consumerName}", package = __package__).configure(config)
        _processtemplate(config, 'void', 'vimrc.aridt', concernvimrc)
        _processtemplate(config, 'pystr', 'loop.py.aridt', looppath)
        _processtemplate(config, 'pystr', 'sendblock.py.aridt', sendblock)
        _processtemplate(config, 'pystr', 'quit.py.aridt', quit)
        _processtemplate(config, 'screenstr', 'screenrc.aridt', screenrc)
        stuffablescreen(config.doubleQuoteKey)[print]('-S', config.sessionName, '-c', screenrc)
