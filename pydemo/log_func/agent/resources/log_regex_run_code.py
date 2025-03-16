import lparser.utils.env
from lparser import conf
conf.DEBUG = False
from lparser.main import tool_regex
from lparser.status import Status, OP, ARG

files = None
file = None
op_map = None
### <FILES> ###


### <CODE> ###


if op_map is None:
    raise Exception('未指定op_mamp')

if file is None:
    if files is None or len(files) == 0:
        raise Exception('未上传log文件')
    file = files[-1]

tool_regex(file, op_map=op_map)
