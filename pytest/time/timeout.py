
# pip install func_timeout

import time
from func_timeout import func_set_timeout,FunctionTimedOut

@func_set_timeout(2)
def test_func():
    time.sleep(3)
    return 'b'


if __name__ == '__main__':
    ret = None
    try:
        ret = test_func()
    except FunctionTimedOut:
        print('FunctionTimedOut')
        pass

    print(ret)
