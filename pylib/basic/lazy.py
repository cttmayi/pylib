

def lazy_property(func):
    attr = "__lazy_" + func.__name__

    @property
    def __lazy_property(self):
        if not hasattr(self, attr):
            setattr(self, attr, func(self))
        return getattr(self, attr)

    return __lazy_property





if __name__ == '__main__': # Test
    
    class P:
        @lazy_property
        def l_A(self):
            print('cal P_A')
            a = 1
            for i in range(1, 10):
                a = a * i
            return a
        
        @property
        def n_A(self):
            print('cal N_A')
            a = 1
            for i in range(1, 10):
                a = a * i
            return a
    
    p = P()
    print(1, p.l_A)
    print(2, p.l_A)
    print(3, p.l_A)
    print(4, p.n_A)
    print(5, p.n_A)
    print(6, p.n_A)
    
    
    
    