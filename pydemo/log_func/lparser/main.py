import lparser.debug as debug
from lparser.parser import LogParser
from lparser.status import Error
from runtime.op import OP_MAPS

def tool_main(path, type=None):
    lp:LogParser = LogParser(path, OP_MAPS, type)
    logs = lp.transfor_to_df()
    if logs is None:
        raise Exception('log格式无法识别')
    debug.file(logs, 'logs')

    ops = lp.transfor_to_op(logs)
    debug.file(ops, 'ops')

    errors = lp.op_execute(ops)

    for level in Error.LEVELS:
        for error in errors:
            if error.level == level:
                print(error.get_error_msg(logs), '\n')
                pass

        return errors, ops, logs
    
    return None


def tool_parser(path, looper):
    lp:LogParser = LogParser(path, OP_MAPS, looper=looper)
    logs = lp.transfor_to_df()
    if logs is None:
        raise Exception('log格式无法识别')

    ops = lp.transfor_to_op(logs)
    lp.op_execute(ops)



def tool_regex(path, op_map):
    lp:LogParser = LogParser(path, op_maps=op_map)
    logs = lp.transfor_to_df()
    if logs is None:
        raise Exception('log格式无法识别')
    
    ops = lp.transfor_to_op(logs)

    print(f'总数量：{len(logs)}, 匹配数量等于{len(ops)}, 匹配的细节如下:')


    # 遍历dataframe ops， 获取里面的line属性，并将logs 对应的行数，设置为和ops的name匹配成功

    logs['match'] = '未能匹配'
    for _, op in ops.iterrows():
        # print(f'line: {op.line}, name: {op.name}, info: {op.info}, args: {op.args}')
        print(f'line: {op.line}, name: {op.opname}')
        logs.loc[op.line, 'match'] = f'和 {op.opname} 匹配成功'

    logs = logs[['msg', 'match']]

    print(logs)
