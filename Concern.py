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

from pathlib import Path
import tempfile, subprocess, sys, aridity, shutil

def main():
    configdir = Path.home() / '.Concern'
    configdir.mkdir(parents = True, exist_ok = True)
    with tempfile.TemporaryDirectory(dir = configdir) as tempdir:
        projectdir = Path(__file__).resolve().parent
        tempdir = Path(tempdir)
        vimrc = tempdir / 'vimrc'
        sendblock = tempdir / 'sendblock.py'
        screenrc = tempdir / 'screenrc'
        context = aridity.Context()
        with aridity.Repl(context) as repl:
            printf = repl.printf
            printf("cd %s", projectdir)
            printf('. Concern.arid')
            printf('Concern')
            printf("\tvimrcPath = %s", vimrc)
            printf("\tsendblock = %s", sendblock)
            args = sys.argv[1:]
            if args:
                printf('\tvimArgs := $list()')
                for arg in args:
                    printf("\tvimArgs += %s", arg)
            printf("redirect %s", vimrc)
            printf('Concern < vimrc.aridt')
            printf("redirect %s", sendblock)
            printf('" = $(pystr)')
            printf('Concern < sendblock.py.aridt')
            printf("redirect %s", screenrc)
            printf('" = $(screenstr)')
            printf('Concern < screenrc.aridt')
        shutil.copy2(projectdir / 'getblock.py', tempdir)
        subprocess.check_call(['screen', '-S', context.resolved('Concern', 'sessionName').value, '-c', screenrc])

if '__main__' == __name__:
    main()
