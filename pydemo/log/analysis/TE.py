'''
TE 稳定相关
'''

from env import Status
from env.display import *

def func(status:Status):
    #if state.get_action_id() == TE:
    if status.get_state(FRAME) == 'START':
        status.wait_action_state(FRAME, 'DONE', 2, 'FRAME 时间过长(3)')


    print(status.get_op_millis(), status.get_millis(TE))
    if 90 < status.get_op_millis() - status.get_millis(TE) > 110:
        return f"TE不稳定"

    return None