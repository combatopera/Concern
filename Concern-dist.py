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
from system import git, zip
from pathlib import Path
import tempfile, shutil, aridity

log = logging.getLogger(__name__)
githuburl = "https://github.com/combatopera"
leafprojectname = 'Concern'

class VersionConflictException(Exception): pass

def main():
    with tempfile.TemporaryDirectory() as tempdir:
        projectsdir = Path(tempdir, 'projects')
        projects = {(leafprojectname, 'master')}
        doneprojects = set()
        while projects != doneprojects:
            remaining = sorted(projects - doneprojects)
            log.info("Remaining: %s", remaining)
            projectname, branch = remaining[0]
            projectpath = projectsdir / projectname
            if projectpath.exists():
                raise VersionConflictException
            git('clone', '--branch', branch, '--single-branch', "%s/%s" % (githuburl, projectname), projectpath)
            context = aridity.Context()
            with aridity.Repl(context) as repl:
                repl.printf('projects := $list()')
                repl.printf('branch := $fork()')
                repl.printf(". %s", projectpath / 'project.arid')
            depbranches = context.resolved('branch').unravel()
            for depname in context.resolved('projects').unravel():
                projects.add((depname, depbranches.get(depname, 'master')))
            doneprojects.add((projectname, branch))
        foldername = "%s-%s" % (
                leafprojectname,
                git('rev-parse', '--short', '@', cwd = projectsdir / leafprojectname).stdout.decode().rstrip())
        for path in projectsdir.glob('*/.git'):
            shutil.rmtree(path)
        projectsdir.rename(projectsdir.parent / foldername)
        zip('-r', Path("%s.zip" % foldername).resolve(), foldername, cwd = tempdir)

if '__main__' == __name__:
    main()
