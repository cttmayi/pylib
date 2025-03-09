class AssignMonitor:
    def __enter__(self):
        self._original_setattr = object.__setattr__
        print('object', object)
        object.__setattr__ = self.custom_setattr
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        object.__setattr__ = self._original_setattr

    def custom_setattr(self, obj, name, value):
        print(f"Assigning {value} to {name}")
        self._original_setattr(obj, name, value)

with AssignMonitor():
    class MyClass:
        pass

    obj = MyClass()
    obj.x = 10  # 输出：Assigning 10 to x