from getblock import readblock
from stufftext import stuff

def main():
    stuff(readblock())

if '__main__' == __name__:
    main()
