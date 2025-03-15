import lparser.debug as debug
from lparser.parser import LogParser
from lparser.status import Error

def tool_main(path, type, looper=None):
    lp:LogParser = LogParser(path, type, looper)
    logs = lp.transfor_to_df()
    debug.file(logs, 'logs')

    ops = lp.transfor_to_op(logs)
    debug.file(ops, 'ops')

    errors = lp.op_execute(ops)

    if looper is None:
        for level in Error.LEVELS:
            for error in errors:
                if error.level == level:
                    print(error.get_error_msg(logs), '\n')
                    pass

        return errors, ops, logs


