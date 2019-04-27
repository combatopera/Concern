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

from system import git, zip
from pathlib import Path
import tempfile, shutil

def main():
    with tempfile.TemporaryDirectory() as dirpath:
        root = Path(dirpath, 'Concern')
        root.mkdir()
        projectname = 'Concern'
        git('clone', '--single-branch', "https://github.com/combatopera/%s" % projectname, root / projectname)
        foldername = "Concern-%s" % git('rev-parse', '--short', '@').stdout.decode().rstrip()
        shutil.rmtree(root / projectname / '.git')
        root.rename(root.parent / foldername)
        zip('-r', Path("%s.zip" % foldername).resolve(), foldername, cwd = dirpath)

if '__main__' == __name__:
    main()
