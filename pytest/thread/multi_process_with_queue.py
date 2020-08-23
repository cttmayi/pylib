

from multiprocessing import Process, Queue


def func_p(q):
    for i in range(5):
        print('q:', i)
        q.put(i)

if __name__ == '__main__':
    q = Queue()

    process_list = []
    for i in range(3):
        p = Process(target=func_p,args=(q,))  #注意args里面要把q对象传给我们要执行的方法，这样子进程才能和主进程用Queue来通信
        p.start()
        process_list.append(p)

    for i in process_list:
        p.join()

    while not q.empty():
        print('c: ', q.get())

    print('Test End')