import os
import importlib

def get_modules(package_path="."):
    modules = []
    files = os.listdir(package_path)
    for file in files:
        if not file.startswith("_"):
            name, _ = os.path.splitext(file)
            modules.append(name)
    return modules


def import_module(module_name, package_name):
    module = importlib.import_module("." + module_name, package_name)
    ret = {}
    for attr in dir(module):
        if not attr.startswith("_"):
            func = getattr(module, attr)
            ret[attr] = func
    return ret

import re

# 简化正则表达式, 用类似printf的方式去匹配

_values = {
    'x': r'([\da-fA-F]{1,})', # 16进制的数字, 不包括前面的0x, 比如 F9, 55
    'd': r'([+-]{0,1}\d{1,})', # 10进制的数字
    's': r'([\da-zA-Z\.]{1,}[\da-zA-Z]{1,})', # 字符串
    'a': r'(.+)',
    'X': r'[\da-fA-F]{1,}',
    'D': r'[+-]{0,1}\d{1,}',
    'S': r'[\da-zA-Z\.]{1,}[\da-zA-Z]{1,}',
    'a': r'.+',
}


class ReExp:
    def __init__(self, cond):
        self._re = re.compile(self._exp(cond))
        self._match_obj = None


    def _exp(self, cond):
        cond_arr = []
        is_replace = False
        for i in range(len(cond)):
            c = cond[i]
            if c == '%':
                is_replace = True
            elif is_replace:
                if c in _values.keys():
                    cond_arr.append(_values[c])
                elif c in ['0', '1']:
                    cond_arr.append('%')
                    cond_arr.append(c)
                is_replace = False
            elif c in [ '(', ')', '\\', '[', ']', '-', '.']:
                cond_arr.append('\\')
                cond_arr.append(c)
            else:
                cond_arr.append(c)    
    
        cond =  ''.join(cond_arr)
        return cond

    def match(self, msg):
        match_obj = self._re.match(msg)
        self._match_obj = match_obj

        return match_obj is not None

    def get(self, id):
        return self._match_obj.group(id + 1) if self._match_obj else None