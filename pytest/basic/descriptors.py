

# 描述器决定了对象属性是如何被访问的。描述器的作用是定制当你想引用一个属性时所发生的操作。

# 构建描述器的方法是至少定义以下三个方法中的一个。需要注意，下文中的instance是包含被访问属性的对象实例，而owner则是被描述器修辞的类。

# __get__(self, instance, owner) – 这个方法是当属性被通过(value = obj.attr)的方式获取时调用，这个方法的返回值将被赋给请求此属性值的代码部分。
# __set__(self, instance, value) – 这个方法是当希望设置属性的值(obj.attr = ‘value’)时被调用，该方法不会返回任何值。
# __delete__(self, instance) – 当从一个对象中删除一个属性时(del obj.attr)，调用此方法。


class Value(object):
    def __init__(self, value=0.0):
        self.value = float(value)
    def __get__(self, instance, owner):
        print('__get__', instance, owner)
        return self.value
    def __set__(self, instance, value):
        print('__set__', instance, value)
        self.value = float(value)
 
class Temperature(object):
    value = Value()
 
temp = Temperature()
v = temp.value