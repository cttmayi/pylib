
class TEValue:
    def __init__(self, value, millis):
        self.value = value      # 存储任意类型的值
        self.millis = millis    # 存储millis属性

    def __repr__(self):
        return repr(self.value)  # 模拟原始值的表现

    def __str__(self):
        return str(self.value)

    # 动态代理所有未定义的操作到 self.value
    def __getattr__(self, name):
        return getattr(self.value, name)

class Status:
    def __init__(self):
        self._te = TEValue(1, 10)  # 初始值 TE=1, millis=10

    @property
    def TE(self):
        return self._te

    @TE.setter
    def TE(self, value):
        # 创建新实例时，保留当前millis的值
        self._te = TEValue(value, self._te.millis)

status = Status()

# 测试动态修改
print(status.TE, status.TE.millis)  # 输出: 1 10

status.TE = 3  # 修改TE值，millis保持10
print(status.TE, status.TE.millis)  # 输出: 3 10

status.TE.millis = 30  # 单独修改millis
print(status.TE, status.TE.millis)  # 输出: 3 30

status.TE = 5  # 再次修改TE，millis保留30
print(status.TE, status.TE.millis)  # 输出: 5 30