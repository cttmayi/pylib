from lenv import Env
from lenv.display import *

def func(env:Env, log):
    if log.msg.startswith('TE'):
        env.state_set(TE, 'T')
    elif log.msg.startswith('FRAME START'):
        env.state_set(FRAME, FRAME_START)
    elif log.msg.startswith('FRAME DONE'):
        env.state_set(FRAME, FRAME_DONE)
    elif log.msg.startswith('DQ BUFFER'):
        env.state_set(BUFFER, BUFFER_DQ, log.msg.split()[-1])
    elif log.msg.startswith('DRAW BUFFER'):
        env.state_set(BUFFER, BUFFER_DRAW, log.msg.split()[-1])
    elif log.msg.startswith('FRAME SKIP'):
        env.state_set(BUFFER, BUFFER_Q, log.msg.split()[-1])


