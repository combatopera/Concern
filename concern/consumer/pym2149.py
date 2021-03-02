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

from lagoon.binary import sh
import shlex

def _getconfig(config, *names):
    command = config.pym2149.shellCommand
    for name in names:
        command += ' --repr ' + shlex.quote(name)
    from collections import OrderedDict
    values = list(map(eval, sh._c(command).splitlines()))
    del OrderedDict
    return values

def configure(config):
    consumerinfo, = _getconfig(config, 'OSC')
    (-config).printf("consumer bufsize = %s", consumerinfo['bufsize'])
    (-config).printf("consumer port = %s", consumerinfo['port'])
