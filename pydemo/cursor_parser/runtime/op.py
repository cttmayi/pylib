import os
# from pylib.basic.file import file_read
from lparser.status import Status, OP, ARG
from lparser.utils.utils import get_modules, import_module

# STATUS_MAP = {
#     # g: None,
#     # d: g
# }

# =========================================================================
# NAME, FUNC_INIT, FUNC, ARGUMENTS, PATTERN
OP_MAP_DEBUG = [
    OP('MODE', 'MODE %d %d', info='mode change', args=['last', 'mode']),
    OP('TE', 'TE', info='表示屏幕TE信号, 无参数'),
    OP('DQ', 'DQ BUFFER %d', info='dequeue buffer', args=[ARG('id', 'buffer id')]),
    OP('Q', 'Q BUFFER %d', info='enqueue buffer', args=[ARG('id', 'buffer id')]),
    OP('DUMP', 'DUMP CMDS'),
]


# regex_full_list_android = file_read('data/android/templates.jsonl')

# OP_MAP_ANDROID = []
# for name, pattern
# , info, args in regex_full_list_android:
#     args_ARG = []
#     for k, v in args.items():
#         args_ARG.append(ARG(k, v))
#     OP_MAP_ANDROID.append(
#         OP(name, pattern, info=info,
#             args=args))


OP_MAPS = {
    'android': OP_MAP_DEBUG,
    # 'android': OP_MAP_ANDROID
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
        

# for status, pstatus in STATUS_MAP.items():
#     status.set_global_status(pstatus)
