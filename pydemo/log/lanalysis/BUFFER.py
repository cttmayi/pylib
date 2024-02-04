from env import Status
from env.display import *

def func_FRAME(status:Status):
    # if state.get_action_id() == FRAME:
    if status.op_state() == BUFFER_DQ:
        status.wait_op_state(FRAME, FRAME_DONE, 200, 'BUFFER 时间过长(1)')

    return None