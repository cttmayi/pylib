import os
import functools
try:
    import diskcache
    user_home = os.path.expanduser("~") # 获取用户主目录
    cache_path = os.path.join(user_home, ".diskcache")
    cache = diskcache.Cache(cache_path)
except ImportError:
    cache = None

def cache_disk(expire=None, ignore_first=False):
    if cache is not None:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if ignore_first:
                    key = (args[1:], frozenset(kwargs.items()))
                else:
                    key = (args, frozenset(kwargs.items()))
                if key in cache:
                    result = cache[key]
                    # if expire is not None:
                    #     cache.set(key, result, expire=expire)
                    return result
                else:
                    result = func(*args, **kwargs)
                    if expire is not None:
                        cache.set(key, result, expire=expire)
                    else:
                        cache[key] = result
                    return result
            return wrapper
    else:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # print("Diskcache not installed, caching is disabled.")
                return func(*args, **kwargs)
            return wrapper

    return decorator

cache_disk_for_class = functools.partial(cache_disk, ignore_first=True)

# 清除缓存
def clear_cache():
    if cache is not None:
        cache.clear()


if __name__ == "__main__":
    import time
    @cache_disk()
    def expensive_function(param):
        print(f"Computing for {param}...")
        time.sleep(param)
        return param * 2

    # 测试
    result1 = expensive_function(3)
    result2 = expensive_function(3)  # 如果安装了 diskcache，这里会命中缓存


    class TestClass:
        @cache_disk()
        def expensive_method(self, param, args=None):
            print(f"Computing_ for {param}...")
            time.sleep(param)
            return param * 2

    test = TestClass()
    result3 = test.expensive_method(2, args="test")
    result4 = test.expensive_method(2)  # 如果安装了 diskcache，这里会命中缓存

    # clear_cache()