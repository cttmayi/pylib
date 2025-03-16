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



