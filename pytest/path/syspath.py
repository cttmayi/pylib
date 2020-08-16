

import os
import sys


# 添加到python执行入口, 可以保证不受到执行路径的影响
path = 'path'
syspath = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
sys.path.insert(0, syspath)


