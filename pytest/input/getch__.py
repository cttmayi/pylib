 
import sys
import select
from time import sleep
import termios
import tty
 
old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

def getch():    
    c = None
    if select.select([sys.stdin], [], [], 0.01) == ([sys.stdin], [], []):
        c = sys.stdin.read(1)
        #if c == '\x1b': break
        #sys.stdout.write(c)
        #sys.stdout.flush()

    #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print(c)
    return c

while True:
    ch = getch()
    if ch is not None:
        print(ord(ch))

    sleep(0.1)
    #print('pppp')