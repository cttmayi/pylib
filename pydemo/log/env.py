from typing import Any
import pandas as pd
import numpy as np


def PRE(id):
    return f"P_{id}"

def PRE_T(id):
    return f"P_T_{id}"

def T(id):
    return f"T_{id}"

class Env:
    def __init__(self):
        self._state = {}
        self._state_freq = {}
        self._state_once = {}
        self._state_millis = {}

    def get_status(self):
        return dict(self._state, **self._state_once)
    
    def reset(self, log):
        self._state_once = {}
        self.log = log
        self._state['time'] = log.time

    def state_set(self, id, state):
        self._state_once[PRE(id)] = self._state.get(id, np.nan)
        self._state_once[PRE_T(id)] = self._state.get(T(id), np.nan)
        self._state[id] = state
        self._state[T(id)] = self.log.millis

    def state_get(self, id):
        return self._state.get(id, None)

    def state_inc(self, id, inc):
        if id in self._state.keys():
            self._state[id] += inc
        else:
            self._state[id] = inc if inc > 0 else 0

    def flow_set(self, id, flow):
        pass

    def state_freq(self, id):
        millis = self.log.millis
        
        if id in self._state_millis.keys():
            millis_ = self._state_millis[id]
            self._state[id] = millis - millis_

        self._state_millis[id] = millis


class State:
    def __init__(self, state) -> None:
        self._state = state
        pass

    def get(self, id):
        val = self._state.get(id)
        # print(val)
        if val is None:
            raise Exception("Ignore")
        return val

    def time(self, id, s1, s2=None):
        s2 = s2 if s2 is not None else s1
        # print(self._state[PRE(id)], self._state[id])
        if self._state[PRE(id)] == s1 and self._state[id] == s2:
            return self._state[T(id)] - self._state[PRE_T(id)]
        raise Exception("Ignore")

        


