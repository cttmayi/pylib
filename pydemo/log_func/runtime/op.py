import os
from pylib.basic.file import file_read
from runtime.ops.g import STATUS as g
from runtime.ops.d import STATUS as d
from lparser.status import Status, OP, ARG
from lparser.utils.utils import get_modules, import_module

STATUS_MAP = {
    g: None,
    d: g
}

# =========================================================================
# NAME, FUNC_INIT, FUNC, ARGUMENTS, PATTERN
# OP_MAP_DEBUG = [
#     OP('MODE', 'MODE %d %d', info='mode change',
#        func_init=g.MODE_INIT, func=g.MODE, args=['last', 'mode']),
#     OP('TE', 'TE', info='表示屏幕TE信号，无参数' ,
#        func = d.TE),
#     OP('DQ', 'DQ BUFFER %d', info='dequeue buffer',
#        func = d.DQ, args=[ARG('id', 'buffer id')]),
#     OP('Q', 'Q BUFFER %d', info='enqueue buffer',
#        func = d.Q, args=[ARG('id', 'buffer id')]),
#     OP('DUMP', 'DUMP CMDS',
#        func = d.DUMP),
#     OP('DUMP', 'REG %d %d %d %d',
#        func = None, args=['v1']), # 同名会自动合并命令， 为保证正确性，必须保证写在一起，且不能有FUNC参数
# ]


regex_full_list_android = file_read('data/android/templates.jsonl')

OP_MAP_ANDROID = []
for regex_full in regex_full_list_android:
    args_ARG = []
    for k, v in regex_full[2].items():
        args_ARG.append(ARG(k, v))
    OP_MAP_ANDROID.append(
        OP(regex_full[0], regex_full[0], info=regex_full[1],
            args=regex_full[2]))


OP_MAPS = {
    # 'debug': OP_MAP_DEBUG,
    'android': OP_MAP_ANDROID
}


# =========================================================================

def get_op_name(id, op_map):
    return op_map[id].name

def get_op_pattern(id, op_map):
    return op_map[id].pattern

def get_op_arguments(id, op_map):
    return op_map[id].arguments

def get_op_func(id, op_map):
    return op_map[id].func

def get_op_func_init(id, op_map):
    return op_map[id].func_init

def get_loopers():
    package_name = 'runtime.looper'
    package_path = os.path.join(os.path.dirname(__file__), 'looper')
    modules = get_modules(package_path)

    looper_func_list = []
    for module_name in modules:
        func = import_module(module_name, package_name)
        for func_name in func.keys():
            if func_name.startswith('looper'):
                looper_func_list.append(func.get(func_name))
    return looper_func_list
        



for status, pstatus in STATUS_MAP.items():
    status.set_global_status(pstatus)
