

from multiprocessing import Process, Pipe
def func_sub(conn):
    conn.send('hi, Main')
    print('Sub Get: ',conn.recv())
    conn.close()

if __name__ == '__main__':
    p1, p2 = Pipe()
    p = Process(target=func_sub, args=(p2,))
    p.start()
    print('Main Get: ', p1.recv())
    p1.send('hi, Sub')
    p.join()
    print('Test End')