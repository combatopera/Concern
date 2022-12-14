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

'Vim-based live coding environment.'
from . import templates
from .util import initlogging
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from aridity.util import openresource
from pathlib import Path
from screen import stuffablescreen
from tempfile import TemporaryDirectory
import logging, os, sys

log = logging.getLogger(__name__)

class Context:

    def __init__(self, config):
        self.contextctrl = -config.context

    def processtemplate(self, quotename, templatename, targetpath):
        cc = self.contextctrl.childctrl()
        cc.printf('" = $(%s)', quotename)
        with openresource(templates.__name__, templatename) as f:
            cc.processtemplate(f, targetpath)

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'Concern.arid', settingsoptional = True)
    parser = ArgumentParser()
    parser.add_argument('--chdir', type = os.path.expanduser)
    _, vimargs = parser.parse_known_args(namespace = config.cli)
    if config.chdir is not None:
        os.chdir(config.chdir)
    configdir = Path.home() / '.config' / 'Concern'
    configdir.mkdir(parents = True, exist_ok = True)
    with TemporaryDirectory(dir = configdir) as tempdir:
        tempdir = Path(tempdir)
        session_vim = tempdir / 'Session.vim'
        looppath = tempdir / 'loop.py'
        sendblock = tempdir / 'sendblock.py'
        quit = tempdir / 'quit.py'
        screenrc = tempdir / 'screenrc'
        config.Session_vim = str(session_vim)
        config.looppath = str(looppath)
        config.sendblock = str(sendblock)
        config.quit = str(quit)
        (-config).printf('vimArgs := $list()')
        for arg in vimargs:
            (-config).printf("vimArgs += %s", arg)
        config.context.signalpath = str(tempdir / 'signal')
        context = Context(config)
        context.processtemplate('void', 'Session.vim.aridt', session_vim)
        context.processtemplate('pystr', 'loop.py.aridt', looppath)
        context.processtemplate('pystr', 'sendblock.py.aridt', sendblock)
        context.processtemplate('pystr', 'quit.py.aridt', quit)
        context.processtemplate('screenstr', 'screenrc.aridt', screenrc)
        stuffablescreen(config.doubleQuoteKey)[print]('-S', config.sessionName, '-c', screenrc, env = dict(PYTHONPATH = os.pathsep.join(sys.path[1:])))

if '__main__' == __name__:
    main()
