from lparser import conf
conf.DEBUG = False
from lparser.parser import LogParser
from runtime.op import OP_MAPS

def tool_parser(path, looper):
    lp:LogParser = LogParser(path, OP_MAPS, looper=looper)
    logs = lp.transfor_to_df()
    if logs is None:
        raise Exception('log格式无法识别')

    ops = lp.transfor_to_op(logs)
    lp.op_execute(ops)

files = None
file = None
### <FILES> ###

def looper(**kwargs):
    raise Exception('未定义looper函数')

### <CODE> ###

if file is None:
    if files is None or len(files) == 0:
        raise Exception('未上传log文件')

    file = files[-1]
tool_parser(file, looper=looper)
