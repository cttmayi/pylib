class AssignMonitor:

    def __init__(self, status):
        self.status = status

    def __enter__(self):
        print('enter', )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit_type', exc_type)
        print('exit_val', exc_val)
        print('exit_tb', exc_tb)

class MyClass:
    pass

class Status:
    pass

s = Status()

with AssignMonitor(s) as monitor:
    obj = MyClass()
    obj.x = 10  # 输出：Assigning 10 to x
    obj.x = obj.y 