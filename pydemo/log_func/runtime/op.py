from runtime.ops.g import STATUS as g
from runtime.ops.d import STATUS as d
from lparser.status import Status, OP, ARG

STATUS_MAP = {
    g: None,
    d: g
}

# =========================================================================
# NAME, FUNC_INIT, FUNC, ARGUMENTS, PATTERN
OP_MAP_DEBUG = [
    OP('MODE', 'MODE %d %d', info='mode change',
       func_init=g.MODE_INIT, func=g.MODE, args=['last', 'mode']),
    OP('TE', 'TE', info='表示屏幕TE信号，无参数' ,
       func = d.TE),
    OP('DQ', 'DQ BUFFER %d', info='dequeue buffer',
       func = d.DQ, args=[ARG('id', 'buffer id')]),
    OP('Q', 'Q BUFFER %d', info='enqueue buffer',
       func = d.Q, args=[ARG('id', 'buffer id')]),
    OP('DUMP', 'DUMP CMDS',
       func = d.DUMP),
    OP('DUMP', 'REG %d %d %d %d',
       func = None, args=['v1', 'v2', 'v3', 'v4']), # 同名会自动合并命令， 为保证正确性，必须保证写在一起，且不能有FUNC参数
]

OP_MAPS = {
    'debug': OP_MAP_DEBUG,
}


# =========================================================================

def get_op_name(type ,id):
    return OP_MAPS[type][id].name

def get_op_pattern(type, id):
    return OP_MAPS[type][id].pattern

def get_op_arguments(type, id):
    return OP_MAPS[type][id].arguments

def get_op_func(type, id):
    return OP_MAPS[type][id].func

def get_op_func_init(type, id):
    return OP_MAPS[type][id].func_init

names = set()
paatterns = set()

PATTERN_LIST = [] # PATTERN, ARGUMENTS

last_name = None
# OP_MAP = [] # TYPE, NAME, FUNC_INIT, FUNC, ARGUMENTS, PATTERN
for type, ops in OP_MAPS.items():
    for op in range(len(ops)):
        name = get_op_name(type, op)
        pattern = get_op_pattern(type, op)
        arguments = get_op_arguments(type, op)
        func_init = get_op_func_init(type, op)
        func = get_op_func(type, op)

        if name in names and not name == last_name:
            raise Exception(f'OP_MAP NAME 重复: {name}')
        names.add(name)
        last_name = name

        if pattern in paatterns:
            raise Exception(f'OP_MAP PATTERN 重复: {pattern}' )
        paatterns.add(pattern)

        PATTERN_LIST.append([pattern, arguments]) # PATTERN, ARGUMENTS
        # OP_MAP.append([type, name, func_init, func, arguments, pattern]) # TYPE, NAME, FUNC_INIT, FUNC, ARGUMENTS, PATTERN

for status, pstatus in STATUS_MAP.items():
    status.set_global_status(pstatus)


if __name__ == '__main__':
    print(PATTERN_LIST)