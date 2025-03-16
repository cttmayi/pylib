import lparser.utils.env
from lparser import conf
conf.DEBUG = False
from lparser.status import Status, OP, ARG
from lparser.parser import LogParser
from lparser.status import Error

def tool_regex(path, op_map):
    lp:LogParser = LogParser(path, op_maps=op_map)
    logs = lp.transfor_to_df()
    if logs is None:
        raise Exception('log格式无法识别')
    
    ops = lp.transfor_to_op(logs)

    print(f'总数量：{len(logs)}, 匹配数量等于{len(ops)}, 匹配的细节如下:')
    logs['match'] = '未能匹配'
    for _, op in ops.iterrows():
        print(f'line: {op.line}, name: {op.opname}')
        logs.loc[op.line, 'match'] = f'和 {op.opname} 匹配成功'
    logs = logs[['msg', 'match']]
    print(logs)

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
