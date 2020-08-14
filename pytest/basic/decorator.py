import functools


# 装饰器

def call(func):
    @functools.wraps(func) # 用于保留函数__name__属性, 否则被装饰的函数的__name__将变为wrapper, 当然一般情况下也不需要此定义
    def wrapper(*args, **kw):
        print('%s() start' % func.__name__)
        ret = func(*args, **kw)
        print('%s() end' % func.__name__)
        return ret
    return wrapper

def call_with_text(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('[%s]%s() start' % (text, func.__name__))
            ret = func(*args, **kw)
            print('[%s]%s() end' % (text, func.__name__))
            return ret
        return wrapper
    return decorator


@call
def call_main():
    print('### main ###')
    pass

@call_with_text('Message')
def call_main_text():
    print('### main ###')
    pass

call_main()
call_main_text()
########################################