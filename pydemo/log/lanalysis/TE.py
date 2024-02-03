'''
TE 稳定相关
'''

from env import Status
from env.display import *

def func(status:Status):
    #if state.get_action_id() == TE:
    if status.state(FRAME) == 'START':
        status.wait_op_state(FRAME, 'DONE', 2, 'FRAME 时间过长(3)')

    if 90 < status.op_millis() - status.millis(TE) > 110:
        return f"TE不稳定"

    return None