import time
import sys


print('PPS')

for i in range(10):
    print('\r\r', str(i)*10, end='', flush=True)
    # sys.stdout.flush()
    time.sleep(0.1)
print('\nPPT', flush=True)


print('\033[1A\r\033[K', end='')