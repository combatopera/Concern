from getblock import readblock, pilcrow, eol
from pym2149 import osctrl
from stufftext import stuff
import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # XXX: Close it?
    sock.sendto(osctrl.Message('/foxdot', [readblock('')]).ser(), ('localhost', 57120))
    text, _ = sock.recvfrom(1024)
    stuff(eol.join(text.decode('utf_8').splitlines()) + pilcrow + eol)

if '__main__' == __name__:
    main()
