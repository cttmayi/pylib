from runtime.func import DStatus

d_status = DStatus()

STATUS_MAP = {
    'D': d_status,
}

# NAME, PATTERN, ARGUMENTS, FUNC
OP_MAP = [
    ['TE', 'TE', [], [d_status.TE]],
    ['DE', 'DQ BUFFER %d', ['id'], [d_status.BQ]],
]



PATTERN_LIST = []
for op in OP_MAP:
        PATTERN_LIST.append([op[1], op[2]])


def get_op_name(id):
    return OP_MAP[id][0]

def get_op_pattern(id):
    return OP_MAP[id][1]

def get_op_arguments(id):
    return OP_MAP[id][2]

def get_op_func(id):
    return OP_MAP[id][3]

if __name__ == '__main__':
    print(PATTERN_LIST)