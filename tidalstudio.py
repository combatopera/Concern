#!/usr/bin/env pyven

import tempfile, subprocess, os, sys, aridity
from aridimpl.model import Function, Text

studiodir = os.path.dirname(os.path.realpath(__file__))

def projectconfpath(args):
    projectconfname = 'studioproject.arid'
    if args:
        projectdir, = args
        return os.path.join(os.path.abspath(projectdir), projectconfname)
    elif os.path.exists(projectconfname):
        return os.path.abspath(projectconfname)
    else:
        return os.path.join(studiodir, projectconfname)

def main():
    projectconf = projectconfpath(sys.argv[1:])
    configdir = os.path.join(os.path.expanduser('~'), '.tidalstudio')
    os.makedirs(configdir, exist_ok = True)
    with tempfile.TemporaryDirectory(dir = configdir) as tempdir:
        vimrc = os.path.join(tempdir, 'vimrc')
        boottidal = os.path.join(tempdir, 'BootTidal.hs')
        sendblock = os.path.join(tempdir, 'sendblock.py')
        screenrc = os.path.join(tempdir, 'screenrc')
        context = aridity.Context()
        def tosamplesdir(context, samples):
            samplesdir = os.path.join(tempdir, 'Dirt-Samples')
            os.mkdir(samplesdir)
            for name, paths in samples.resolve(context).unravel().items():
                if not hasattr(paths, 'items'): continue # TODO: This is a hack.
                path = os.path.join(samplesdir, name)
                os.mkdir(path)
                for target in paths:
                    os.symlink(target, os.path.join(path, os.path.basename(target)))
            return Text(samplesdir)
        context['tidalstudio', 'toSamplesDir'] = Function(tosamplesdir)
        with aridity.Repl(context) as repl:
            printf = repl.printf
            printf("cd %s", studiodir)
            printf('. tidalstudio.arid')
            printf('tidalstudio')
            printf("\tvimrcPath = %s", vimrc)
            printf("\tBootTidal = %s", boottidal)
            printf("\tsendblock = %s", sendblock)
            printf("\t. %s", projectconf)
            printf("redirect %s", vimrc)
            printf('tidalstudio < vimrc.aridt')
            printf("redirect %s", boottidal)
            printf('tidalstudio tidal < BootTidal.hs.aridt')
            printf("redirect %s", sendblock)
            printf('" = $(pystr)')
            printf('tidalstudio < sendblock.py.aridt')
            printf("redirect %s", screenrc)
            printf('" = $(screenstr)')
            printf('tidalstudio < screenrc.aridt')
        subprocess.check_call(['screen', '-S', context.resolved('tidalstudio', 'sessionName').value, '-c', screenrc])

if '__main__' == __name__:
    main()
