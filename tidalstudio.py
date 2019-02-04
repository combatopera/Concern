#!/usr/bin/env pyven

from pathlib import Path
import tempfile, subprocess, os, sys, aridity

def main():
    configdir = Path.home() / '.tidalstudio'
    configdir.mkdir(parents = True, exist_ok = True)
    with tempfile.TemporaryDirectory(dir = configdir) as tempdir:
        vimrc = os.path.join(tempdir, 'vimrc')
        sendblock = os.path.join(tempdir, 'sendblock.py')
        screenrc = os.path.join(tempdir, 'screenrc')
        context = aridity.Context()
        with aridity.Repl(context) as repl:
            printf = repl.printf
            printf("cd %s", Path(__file__).resolve().parent)
            printf('. tidalstudio.arid')
            printf('tidalstudio')
            printf("\tvimrcPath = %s", vimrc)
            printf("\tsendblock = %s", sendblock)
            printf("redirect %s", vimrc)
            printf('tidalstudio < vimrc.aridt')
            printf("redirect %s", sendblock)
            printf('" = $(pystr)')
            printf('tidalstudio < sendblock.py.aridt')
            printf("redirect %s", screenrc)
            printf('" = $(screenstr)')
            printf('tidalstudio < screenrc.aridt')
        subprocess.check_call(['screen', '-S', context.resolved('tidalstudio', 'sessionName').value, '-c', screenrc])

if '__main__' == __name__:
    main()
