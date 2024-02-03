'''
TE 稳定相关
'''

from env import Status
from env.display import *

def func_TE_frame(status:Status):
    if status.state(FRAME) == FRAME_START:
        status.wait_op_state(FRAME, FRAME_DONE, 2, 'FRAME 时间过长(3)')


def func_TE_stable(status:Status):
    if 90 < status.op_millis() - status.millis(TE) > 110:
        return f"TE不稳定"

    return None