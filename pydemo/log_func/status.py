
class Error:
    def __init__(self, line, msg):
        self.line = line
        self.msg = msg
        self.related_lines = set()
        self.related_lines.add(line)


    def add_related_line(self, line):
        if isinstance(line, int):
            self.related_lines.add(line)

    def __str__(self):
        return f'Error at line {self.line}: {self.msg}'

    def get_error_msg(self, log_df = None):
        related_lines = sorted(self.related_lines)
        related_lines = [line for line in related_lines if line >= 0]
        if log_df is not None:
            return f'Error at line {self.line}: {self.msg}\nRelated lines:\n{log_df.loc[related_lines]}'
        else:
            return f'Error at line {self.line}: {self.msg}\nRelated lines: {related_lines}'

class Value:
    def __init__(self, status, value=None, millis=0, line=-1):
        self._status = status  # 存储status属性
        self.value = value      # 存储任意类型的值
        # self.millis = self.object(value, millis)    # 存储millis属性
        # self.line = self.object(value, line)      # 存储line属性

        self.millis = millis    # 存储millis属性
        self.line = line      # 存储line属性

    # def object(self, val, default=None):
    #     if isinstance(val, dict):
    #         return {k: default for k in val}
    #     elif isinstance(val, (list, tuple)):
    #         return type(val)([default] * len(val))
    #     else:
    #         return default

    def __is__(self, other):
        return self.value is other
    
    def __hash__(self):
        return hash(self.value)
    
    def __bool__(self):
        return bool(self.value)

    def __set__(self, key, value):
        print(f'Setting {key} to {value}')
        self.value[key] = value


    def __eq__(self, other):
        # 如果对方是 TEValue 实例，则比较其 value；否则直接比较 value 和 other
        if isinstance(other, Value):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not (self == other)

    
    def __ge__(self, other):
        if isinstance(other, Value):
            return self.value >= other.value
        return self.value >= other

    def __le__(self, other):
        if isinstance(other, Value):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, Value):
            return self.value > other.value
        return self.value > other

    def __lt__(self, other):
        if isinstance(other, Value):
            return self.value < other.value
        return self.value < other
    
    def __add__(self, other):
        self.millis = self._status.current_millis
        self.line = self._status.current_line
        return self.value + other

    __radd__ = __add__  # 支持反向加法（如 other + self.value）

    def __sub__(self, other):
        self.millis = self._status.current_millis
        self.line = self._status.current_line
        return self.value - other

    __rsub__ = __sub__  # 支持反向减法（如 other - self.value）

    # 代理容器操作（如字典/列表的下标访问）
    def __getitem__(self, key):
        return self.value[key]

    # def __setitem__(self, key, value):
    #     self.millis = self._status.current_millis
    #     self.line = self._status.current_line
    #     self.value[key] = value

    # def __delitem__(self, key):
    #     del self.millis[key]
    #     del self.line[key]
    #     del self.value[key]

    # def append(self, item):
    #     self.millis.append(self._status.current_millis)
    #     self.line.append(self._status.current_line)
    #     self.value.append(item)

    # 代理其他常见容器方法（可选）
    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)

    def __contains__(self, item):
        return item in self.value

    def __repr__(self):
        return repr(self.value)  # 直接返回 value 的表示

    def __str__(self):
        return str(self.value)

    # 动态代理未定义的操作到 self.value（例如属性访问、方法调用）
    def __getattr__(self, name):
        return getattr(self.value, name)



class Status:
    def __init__(self):
        self.value_list = set()
        self.current_millis = 0
        self.current_line = 0
        self.__setattr_func__ = None
        self.__getattribute_func__ = None

        self.enable_attribute__mode()
        self.init_attribute()
        self.disable_attribute_mode()

    def init_attribute(self):
        raise NotImplementedError

    def set_current_info(self, millis, line_number):
        self.current_millis = millis
        self.current_line = line_number

    def get_status(self, value_list):
        values = {}
        millis = {}
        for key in value_list:
            if isinstance(self.__dict__[key], Value):
                values[key] = self.__dict__[key].value
                millis[key] = self.__dict__[key].millis
            elif isinstance(self.__dict__[key], list) or isinstance(self.__dict__[key], dict):
                v, m = self.get_status(self.__dict__[key])
                values.extend(v)
                millis.extend(m)
            else:
                values[key] = self.__dict__[key]
        return values, millis


    def get_all_status(self):
        values, millis = self.get_status(self.value_list)        
        return {'values': values, 'millis': millis}

    def enable_attribute__mode(self):
        self.__setattr_func__ = self.__attribute_setattr__

    # 打开保护模式，禁止动态添加属性
    def disable_attribute_mode(self):
        self.__setattr_func__ = self.__protected_setattr__

    def __setattr__(self, name, value):
        if self.__dict__.get('__setattr_func__') is not None:
            self.__setattr_func__(name, value)
        else:
            super().__setattr__(name, value)

    def __attribute_setattr__(self, name, value):
        #if key not in self.__dict__ and isinstance(value, Value):
        self.value_list.add(name)
        super().__setattr__(name, value)

    def __protected_setattr__(self, name, value):
        if name not in self.__dict__:
            raise AttributeError(f"Cannot set new attribute '{name}' dynamically")
        if name in self.value_list:
            self.__dict__[name] = Value(self, value, self.current_millis, self.current_line)
        else:
            super().__setattr__(name, value)

if __name__ == '__main__':
    import sys


    class OBJ(Status):
        def init_attribute(self):
            self.TE = Value(self)
    status = OBJ()
    status.set_current_info(10, 1)
    # 初始状态
    assert status.TE == None, f'TE should be None, but got {status.TE}'
    # assert status.TE is None, f'TE should be None, but got {status.TE}'
    assert status.TE.millis == 0

    # 修改 TE 为 数字
    status.set_current_info(20, 2)
    status.TE = 1
    assert(status.TE == 1)
    assert(status.TE < 2)
    assert(status.TE.millis == 20)

    status.set_current_info(25, 2)
    status.TE += 2
    assert(status.TE == 3)
    assert(status.TE.millis == 25)

    status.set_current_info(26, 2)
    status.TE -= 3
    assert(status.TE == 0)
    assert(status.TE.millis == 26)

    # 修改 TE 为字符串
    status.set_current_info(20, 2)
    status.TE = "obj"
    assert(status.TE == "obj") 
    assert(len(status.TE) == 3)
    assert(status.TE[0] == "o")
    assert(status.TE.millis == 20)

    print(status.get_all_status())
    print("test pass!")