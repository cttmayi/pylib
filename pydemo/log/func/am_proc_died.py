
from env import Env


def func(env:Env, log):
    env.state_inc("proc", -1)

    env.state_set("am_proc", 'died')

