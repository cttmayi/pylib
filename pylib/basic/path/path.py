import os
import sys


# 选择可执行文件的完整路径
def find_executable(executable):
    paths = os.environ['PATH'].split(os.pathsep)
    if sys.platform == 'win32':
        executable = executable + '.exe'
    for path in paths:
        file = os.path.join(path, executable)
        if os.path.isfile(file):
            return file
    return None


def find_basepath(fstr, path):
    path = os.path.abspath(path)

    if os.path.isfile(path):
        path = os.path.dirname(path)

    basepath = None
    temp = path
    while(True):
        if fstr == os.path.basename(path):
            basepath = temp
            break
        temp = os.path.dirname(path)
        if temp == path:
            break
        path = temp

    return basepath


if __name__ == '__main__':
    print(find_executable('adb'))
    print(find_basepath('pylib', __file__))