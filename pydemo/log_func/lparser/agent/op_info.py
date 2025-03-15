from runtime.op import OP_MAPS


def get_op_infos(type=None):
    ret = {}
    type_list = []
    if type is None:
        type_list = OP_MAPS.keys()
    else:
        type_list = [type]

    for type in type_list:
        ops = OP_MAPS[type]
        for op in ops:
            if op.name not in ret:
                info = op.op_info()
                if info is not None:
                    ret[op.name] = info
    return [ op_info for op_info in ret.values()]
