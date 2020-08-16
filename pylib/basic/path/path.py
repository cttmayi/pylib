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




if __name__ == '__main__':
    print(find_executable('adb'))
    print(__file__)