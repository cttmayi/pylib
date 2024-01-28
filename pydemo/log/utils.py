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
