import sys


#end = ''

def rprint(*arg):
    msg = ' '.join(map(str,arg))
    #global end
    sys.stdout.write('\r\033[K')
    sys.stdout.write(msg)
    sys.stdout.flush()
    #end = '\n'

def print(*arg):
    msg = ' '.join(map(str,arg))

    #global end
    #sys.stdout.write(end)
    #end  = ''
    sys.stdout.write('\r\033[K')
    sys.stdout.write(msg)
    sys.stdout.write('\n')
    sys.stdout.flush()



if __name__ == '__main__':
    import time
    for i in range(20):
        #print('hide')
        rprint('P:' + '*' * i, i)
        #print('show', i)
        time.sleep(0.05)
    print()