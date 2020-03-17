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

from lagoon.binary import bash
import aridity, shlex

def _getconfig(context, *names):
    command = context.resolved('Concern', 'pym2149', 'shellCommand').value
    for name in names:
        command += ' --repr ' + shlex.quote(name)
    from collections import OrderedDict
    values = list(map(eval, bash._c(command).splitlines()))
    del OrderedDict
    return values

def configure(context):
    consumerinfo, = _getconfig(context, 'OSC')
    with aridity.Repl(context) as repl:
        printf = repl.printf
        printf('Concern consumer')
        printf("\tbufsize = %s", consumerinfo['bufsize'])
        printf("\tport = %s", consumerinfo['port'])
