import lparser.utils.env
from lparser.parser import LogParser
from runtime.op import OP_MAPS
from looper import looper

def tool_main_looper(path, type=None):

    loopers = [looper]

    lp:LogParser = LogParser(path, OP_MAPS, type=type, looper=loopers)
    logs = lp.transfor_to_df()
    if logs is None:
        raise Exception('log格式无法识别')

    ops = lp.transfor_to_op(logs)
    lp.op_execute(ops)


if __name__ == '__main__':
    tool_main_looper('data/log/simple.log')