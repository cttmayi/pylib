
from env import Status
from env.display import *

def func(status:Status):
    # if state.get_action_id() == FRAME:
    if status.get_op_state() == 'START':
        status.wait_action_state(FRAME, 'DONE', 1, 'FRAME 时间过长(1)')

    #elif status.get_action_state() == 'DONE':
    #    if status.get_action_millis() - status.get_millis(FRAME) > 100:
    #        return f"FRAME 时间过长(2)"

    return None