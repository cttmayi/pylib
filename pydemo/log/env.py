import pandas as pd


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
        self.state_set('datetime', log.time)

    def state_set(self, id, state):
        self._state[id] = state

    def state_inc(self, id, inc):
        if id in self._state.keys():
            self._state[id] += inc
        else:
            self._state[id] = inc

    def state_freq(self, id):
        now = self.log.datetime
        millis = now.timestamp() * 1000
        
        if id in self._state_millis.keys():
            millis_ = self._state_millis[id]
            self._state[id] = millis - millis_

        self._state_millis[id] = millis