
from multiprocessing import Pool
import os
import time

def worker(num):
    for _ in range(2):
        print("pid=%d, num=%d"%(os.getpid(), num))
        time.sleep(1)

def main():
    pool = Pool(3)  #定义进程池, 设定最大进程数3

    for i in range(10):
        print("start: %d" % (i))
        pool.apply_async(worker, [i,])

    pool.close() # 关闭后不能再添加
    pool.join() # 等待全部进程完毕


print('init', __name__)
if __name__ == '__main__':
    print('main------')
    main()