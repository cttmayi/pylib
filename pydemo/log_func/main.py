import utils.env
import debug
import conf

from parser import LogParser
from status import Error

#获取参数
if conf.DEBUG:
    path = 'log/simple.log'
    type = 'debug'
else:
    import argparse
    parser = argparse.ArgumentParser(description='Parser for log file')
    parser.add_argument('path', type=str, help='log file path')
    parser.add_argument('type', type=str, help='log type')
    args = parser.parse_args()
    path = args.path
    type = args.type

def main(path, type, looper=None):
    lp:LogParser = LogParser(path, type, looper)
    logs = lp.transfor_to_df()
    debug.file(logs, 'logs')

    ops = lp.transfor_to_op(logs)
    debug.file(ops, 'ops')

    errors = lp.op_execute(ops)
    return errors


if __name__ == '__main__':
    errors = main(path, type)

    for level in Error.LEVELS:
        for error in errors:
            if error.level == level:
                print(error.get_error_msg(logs), '\n')
                pass

