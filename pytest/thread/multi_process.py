
from multiprocessing import Process

def func_process(name):
    print('Test %s Multi Processing' % (name))


if __name__ == '__main__':
    process_list = []
    for i in range(5):
        p = Process(
            target=func_process, 
            args=('P' + str(i), )
            )
        p.start()
        process_list.append(p)

    for i in process_list:
        p.join()

    print('Test Finish')