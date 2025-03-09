from runtime.ops.g import STATUS as g
from runtime.ops.disp import STATUS as d


STATUS_GLOBAL = g

STATUS_MAP = {
    'D': d,
}

# NAME, FUNC_INIT, FUNC, ARGUMENTS, PATTERN
OP_MAP_MAIN = [
    ['MODE',    [g.MODE_INIT],  [g.MODE],   ['last', 'mode'],       'MODE %d %d'],
    ['TE',      [],             [d.TE],     [],                     'TE'],
    ['DQ',      [],             [d.DQ],     ['id'],                 'DQ BUFFER %d'],
    ['Q',       [],             [d.Q],      ['id'],                 'Q BUFFER %d'],
]

OP_MAPS = {
    'main': OP_MAP_MAIN,
}


# =========================================================================

def get_op_name(type ,id):
    return OP_MAPS[type][id][0]

def get_op_pattern(type, id):
    return OP_MAPS[type][id][4]

def get_op_arguments(type, id):
    return OP_MAPS[type][id][3]

def get_op_func(type, id):
    return OP_MAPS[type][id][2]

def get_op_func_init(type, id):
    return OP_MAPS[type][id][1]

names = set()
paatterns = set()

PATTERN_LIST = [] # PATTERN, ARGUMENTS
# OP_MAP = [] # TYPE, NAME, FUNC_INIT, FUNC, ARGUMENTS, PATTERN
for type, ops in OP_MAPS.items():
    for op in range(len(ops)):
        name = get_op_name(type, op)
        pattern = get_op_pattern(type, op)
        arguments = get_op_arguments(type, op)
        func_init = get_op_func_init(type, op)
        func = get_op_func(type, op)

        if name in names:
            raise Exception(f'OP_MAP NAME 重复: {name}')
        names.add(name)

        if pattern in paatterns:
            raise Exception(f'OP_MAP PATTERN 重复: {pattern}' )
        paatterns.add(pattern)

        PATTERN_LIST.append([pattern, arguments]) # PATTERN, ARGUMENTS
        # OP_MAP.append([type, name, func_init, func, arguments, pattern]) # TYPE, NAME, FUNC_INIT, FUNC, ARGUMENTS, PATTERN

for status in STATUS_MAP.values():
    status.set_global_status(STATUS_GLOBAL)


if __name__ == '__main__':
    print(PATTERN_LIST)