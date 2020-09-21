

# https://docs.python.org/zh-cn/3/reference/datamodel.html

class Number(object):
    def __init__(self, x, y, z, label):
        self.x = x
        self.y = y
        self.z = z
        self.label = label

        self.sum = x ** 2 + y ** 2 + z ** 2

    # x < y
    def __lt__(self, other):
        print('__lt__', self.label, other.label)
        return self.sum < other.sum

    # x <= y 
    def __le__(self, other):
        return self.sum <= other.sum

    # x == y
    def __eq__(self, other):
        return self.sum == other.sum

    # x != y
    def __ne__(self, other):
        return self.sum != other.sum

    # x > y
    def __gt__(self, other):
        print('__gt__', self.label, other.label)
        return self.sum > other.sum

    # x >= y
    def __ge__(self, other):
        return self.sum >= other.sum

    def __bool__(self):
        print('__bool__', self.label)
        return self.sum != 0


    # (+, -, *, @, /, //, %, divmod(), pow(), **, <<, >>, &, ^, |)
    # object.__add__(self, other)
    # object.__sub__(self, other)
    # object.__mul__(self, other)
    # object.__matmul__(self, other)
    # object.__truediv__(self, other)
    # object.__floordiv__(self, other)
    # object.__mod__(self, other)
    # object.__divmod__(self, other)
    # object.__pow__(self, other[, modulo])
    # object.__lshift__(self, other)
    # object.__rshift__(self, other)
    # object.__and__(self, other)
    # object.__xor__(self, other)
    # object.__or__(self, other)

    # x + y
    def __add__(self, other):
        print('__add__', self.label, other.label)
        return Number(self.x + other.x, self.y + other.y, self.z + other.z, 'sum')
    
    # x & y
    def __and__(self, other):
        print('__and__', self.label, other.label)
        return (self.sum != 0) and (other.sum != 0)

    # (+=, -=, *=, @=, /=, //=, %=, **=, <<=, >>=, &=, ^=, |=)
    # object.__iadd__(self, other)
    # object.__isub__(self, other)
    # object.__imul__(self, other)
    # object.__imatmul__(self, other)
    # object.__itruediv__(self, other)
    # object.__ifloordiv__(self, other)
    # object.__imod__(self, other)
    # object.__ipow__(self, other[, modulo])
    # object.__ilshift__(self, other)
    # object.__irshift__(self, other)
    # object.__iand__(self, other)
    # object.__ixor__(self, other)
    # object.__ior__(self, other)



z = Number(0,0,0, 'z')
a = Number(1,1,1, 'a')
b = Number(2,2,2, 'b')

c = a + b

print('b > a = ', b > a)
print('c > a = ', c < a)
print('not a = ', not a)
print('not z = ', not z)
print('a & b = ', a & b)