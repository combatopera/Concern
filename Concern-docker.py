#!/usr/bin/env python3

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
import argparse, os, subprocess, json, sys

def _commonparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default = 'Concern')
    return parser

def _getgeneration(fetch):
    imageids = subprocess.check_output(['docker', 'images', '--all', '--quiet']).splitlines()
    if imageids:
        # Do not check exit status in case we race removal of an image:
        inspect = subprocess.Popen(['docker', 'image', 'inspect'] + imageids, stdout = subprocess.PIPE)
        prefix = 'CONCERN_GENERATION='
        generations = [int(entry[len(prefix):])
                for image in json.loads(inspect.communicate()[0].decode())
                for entry in image['Config']['Env'] if entry.startswith(prefix)]
        if generations:
            return max(generations) + fetch
    return 1

def install(cmdargs): # TODO LATER: Mac and/or Windows host support.
    parser = _commonparser()
    parser.add_argument('--fetch', action = 'store_true')
    config = parser.parse_args(cmdargs)
    username, = subprocess.check_output(['id', '-un']).decode().splitlines()
    groupname, = subprocess.check_output(['id', '-gn']).decode().splitlines()
    subprocess.check_call(['docker', 'build',
            '--build-arg', "EUID=%s" % os.geteuid(), '--build-arg', "EGID=%s" % os.getegid(),
            '--build-arg', "USERNAME=%s" % username, '--build-arg', "GROUPNAME=%s" % groupname,
            '--build-arg', "GENERATION=%s" % _getgeneration(config.fetch),
            '--tag', imagename, str(Path(__file__).parent / 'container')])
    subprocess.check_call(['docker', 'create',
            '--name', config.name,
            '--device', '/dev/snd',
            '--volume', "%s:/home/%s" % (Path.home(), username),
            '--interactive', '--tty', imagename]) # XXX: Are interactive/tty necessary for both create and exec?
    subprocess.check_call(['docker', 'start', config.name])

def uninstall(cmdargs):
    parser = _commonparser()
    config = parser.parse_args(cmdargs)
    subprocess.check_call(['docker', 'rm', '--force', config.name])

imagename = 'concern'
commands = {f.__name__: f for f in [install, uninstall]}

def main():
    args = sys.argv[1:]
    if args:
        command = commands.get(args[0])
        if command is not None:
            return command(args[1:])
    parser = _commonparser()
    config, fwdargs = parser.parse_known_args(args)
    subprocess.check_call(['docker', 'start', config.name]) # Idempotent.
    # TODO LATER: Allow run from outside home directory assuming absolute paths in args.
    argv = ['docker', 'exec', '--interactive', '--tty', config.name,
            '/opt/Concern/Concern.py',
            '--chdir', "~/%s" % str(Path.cwd().relative_to(Path.home())).replace(os.sep, '/')] + fwdargs
    os.execvp(argv[0], argv)

if '__main__' == __name__:
    main()
