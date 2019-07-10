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

from Concern.initlogging import logging
from system import git, zip, wget, unzip
from pathlib import Path
import tempfile, shutil, aridity

log = logging.getLogger(__name__)
githuburl = "https://github.com/combatopera"
leafprojectname = 'Concern'
shorthashlen = 7

class VersionConflictException(Exception): pass

class ObstructionException(Exception): pass

def main():
    longhash = git('ls-remote', "%s/%s" % (githuburl, leafprojectname), 'master').stdout.decode()[:40]
    projects = {(leafprojectname, longhash), ('pyven', 'master')}
    foldername = "%s-%s" % (leafprojectname, longhash[:shorthashlen])
    zippath = Path("%s.zip" % foldername)
    if zippath.exists():
        raise ObstructionException(zippath)
    with tempfile.TemporaryDirectory() as tempdir:
        ziproot = Path(tempdir, foldername)
        shutil.copytree(Path(__file__).parent / 'skel', ziproot)
        projectsdir = ziproot / 'projects'
        projectsdir.mkdir()
        doneprojects = set()
        deps = set()
        while projects != doneprojects:
            remaining = sorted(projects - doneprojects)
            log.info("Remaining: %s", remaining)
            projectname, branch = remaining[0]
            projectpath = projectsdir / projectname
            if projectpath.exists():
                raise VersionConflictException
            wget("%s/%s/archive/%s.zip" % (githuburl, projectname, branch), cwd = projectsdir)
            unzip("%s.zip" % branch, cwd = projectsdir)
            (projectsdir / ("%s-%s" % (projectname, branch))).rename(projectpath)
            (projectsdir / ("%s.zip" % branch)).unlink()
            context = aridity.Context()
            with aridity.Repl(context) as repl:
                repl.printf('projects := $list()')
                repl.printf('branch := $fork()')
                repl.printf('deps := $list()')
                repl.printf(". %s", projectpath / 'project.arid')
            deps.update(context.resolved('deps').unravel())
            depbranches = context.resolved('branch').unravel()
            for depname in context.resolved('projects').unravel():
                projects.add((depname, depbranches.get(depname, 'master')))
            for name in '.gitignore', '.flakesignore', '.travis.yml':
                path = projectpath / name
                if path.exists():
                    path.unlink()
            with (projectpath / '.pyven.arid').open('w') as f:
                print("branch = %s" % aridity.Repl.quote(branch), file = f)
            doneprojects.add((projectname, branch))
        with (ziproot / '.requirements.txt').open('w') as f:
            for dep in sorted(deps):
                print(dep, file = f)
        zip('-r', zippath.resolve(), foldername, cwd = tempdir)

if '__main__' == __name__:
    main()
