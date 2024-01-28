import sys
import tty
import termios
import select
import os

settings = termios.tcgetattr(sys.stdin)


def getch():
    #tty.setraw(sys.stdin.fileno())
    sys.stdin.fileno()

    ch = None
    if select.select([sys.stdin, ], [], [], 0.0)[0]:
        ch =  sys.stdin.read(1)
    
    if ch is not None and ord(ch) == 3:
        os._exit(0)

    # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return ch








while(True):
    c = getch()
    if c is not None:
        print(ord(c))

