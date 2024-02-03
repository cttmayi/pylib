from env import Env
from env.display import *

def func(env:Env, log):
    if log.msg.startswith('TE'):
        env.state_set(TE, 'T')
    elif log.msg.startswith('FRAME START'):
        env.state_set(FRAME, 'START')
    elif log.msg.startswith('FRAME DONE'):
        env.state_set(FRAME, 'DONE')


