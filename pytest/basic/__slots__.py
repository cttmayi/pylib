


class ClassA(object):
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier

class ClassB(object):
    __slots__ = ['name', 'identifier']
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier
        self.attr = 'attr'


if __name__ == '__main__':
    # print(ClassA.__slots__)
    print(ClassB.__slots__)

    B = ClassB('N', 1)