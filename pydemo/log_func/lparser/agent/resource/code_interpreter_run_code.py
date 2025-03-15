from lparser import conf
conf.DEBUG = False
from lparser.main import tool_main

files = None
### <FILES> ###

def looper(**kwargs):
    raise Exception('未定义looper函数')

### <CODE> ###

if files is None or len(files) == 0:
    raise Exception('未上传log文件')

file = files[-1]
tool_main(file, looper=looper)
