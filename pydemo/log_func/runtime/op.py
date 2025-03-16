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

def get_op_name(type ,id, op_maps):
    return op_maps[type][id].name

def get_op_pattern(type, id, op_maps):
    return op_maps[type][id].pattern

def get_op_arguments(type, id, op_maps):
    return op_maps[type][id].arguments

def get_op_func(type, id, op_maps):
    return op_maps[type][id].func

def get_op_func_init(type, id, op_maps):
    return op_maps[type][id].func_init


for status, pstatus in STATUS_MAP.items():
    status.set_global_status(pstatus)
