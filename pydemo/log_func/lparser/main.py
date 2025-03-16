import lparser.debug as debug
from lparser.parser import LogParser
from lparser.status import Error
from runtime.op import OP_MAPS, get_loopers

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



def tool_main_looper(path, type=None):

    loopers = get_loopers()

    lp:LogParser = LogParser(path, OP_MAPS, type=type, looper=loopers)
    logs = lp.transfor_to_df()
    if logs is None:
        raise Exception('log格式无法识别')

    ops = lp.transfor_to_op(logs)
    lp.op_execute(ops)