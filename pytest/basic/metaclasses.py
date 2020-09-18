

class demo(object):
    pass
 
obj = demo()
 
print("Class of obj is {0}".format(obj.__class__))
print("Class of obj is {0}".format(demo.__class__))
 
# Class of obj is <class '__main__.demo'>
# Class of obj is <type 'type'>