

import sys
import traceback


def func_exception():
    raise NameError("func_exception")


def try_except_main():
    try:
        func_exception()
    except:
        traceback.print_exc(limit=10, file=sys.stdout)
        

if __name__ == '__main__':
    print('-------------------')
    try_except_main()

    print('-------------------')
    func_exception()