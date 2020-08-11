import time

#计算时间函数  
def func_time(func):  
    def wrapper(*args, **kw):  
        local_time = time.time()  
        func(*args, **kw) 
        print('[Perf]%s: %.6f' % (func.__name__ ,time.time() - local_time))
    return wrapper



if __name__ == '__main__':
    @func_time
    def sum(r):
        s = 0
        for i in range(r):
            s = s + i
        return s

    sum(1000000)



