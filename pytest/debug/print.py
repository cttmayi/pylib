from colorama import Fore

print("NORMAL")
print(Fore.GREEN + "GREEN")
print(Fore.BLUE + "BLUE")

print(Fore.YELLOW + "YELLOW")
print(Fore.CYAN + "CYAN")
print(Fore.RED + "RED")
print(Fore.RESET, end='')
print("RESET")

import sys,time
for i in range(100):
    k = i + 1
    s = '|' + '>'*i + ' '*(100-k)+'|'
    sys.stdout.write('\r'+s+f'{i+1}%')
    sys.stdout.flush()
    time.sleep(0.1)