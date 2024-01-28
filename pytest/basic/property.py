


class ClassKey():
    def __init__(self):
        self._key = 'values'


    @property
    def keys(self):
        return self._key
    

    # 变量形式访问， 类似可以做到需要时候计算
    @property
    def vkeys(self):
        return 'Key:' + self._key

key = ClassKey()

print(key.keys)
print(key.vkeys)