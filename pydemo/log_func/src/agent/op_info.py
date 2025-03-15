from runtime.op import OP_MAPS


def get_op_info(type):
    ret = []
    ops = OP_MAPS[type]
    for op in ops:
        info = op.op_info()
        if info is not None:
            ret.append(info)
    return ret