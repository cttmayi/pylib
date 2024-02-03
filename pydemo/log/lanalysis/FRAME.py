from env import Status
from env.display import *

def func_FRAME(status:Status):
    # if state.get_action_id() == FRAME:
    if status.op_state() == FRAME_START:
        status.wait_op_state(FRAME, FRAME_DONE, 200, 'FRAME 时间过长(1)')

    return None