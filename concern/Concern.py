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

'Vim-based live coding environment.'
from . import templates
from .util import initlogging
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from aridity.util import openresource
from pathlib import Path
from screen import stuffablescreen
from tempfile import TemporaryDirectory
import logging, os

log = logging.getLogger(__name__)
configdir = Path.home() / '.config' / 'Concern'

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'Concern.arid', settingsoptional = True)
    parser = ArgumentParser()
    parser.add_argument('--chdir', type = os.path.expanduser)
    parser.add_argument('--session', default = 'Concern')
    _, vimargs = parser.parse_known_args(namespace = config.cli)
    for arg in vimargs:
        (-config).printf("window vim args += %s", arg)
    if config.chdir is not None:
        os.chdir(config.chdir)
    configdir.mkdir(parents = True, exist_ok = True)
    with TemporaryDirectory(dir = configdir) as sessiondir:
        config.sessiondir = sessiondir
        for c in config.T:
            with openresource(templates.__name__, c.templatename) as f:
                (-c.context).processtemplate(f, c.P)
        stuffablescreen(config.doubleQuoteKey)[print]('-S', config.sessionName, '-c', config.T.screenrc.P)

if '__main__' == __name__:
    main()
