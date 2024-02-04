
OP_ID = '_OP_ID'
OP_OBJ = '_OP_OBJ'
OP_STATE = '_OP_STATE'
OP_MILLIS = '_OP_MILLIS'
TIME  = '_TIME'

from lanalysis import LogAnalysis

class Env:
    def __init__(self, la):
        self._state = {}
        self._op = {}
        self.la:LogAnalysis = la

    def get_result(self):
        return self._result

    def reset(self, log):
        self._result = []
        self._op = {}
        self.log = log
        self._op[TIME] = log.time

    def state_set(self, id, state, obj=''):
        self._op[OP_ID] = id
        self._op[OP_STATE] = state
        self._op[OP_MILLIS] = self.log.millis

        self._op[OP_OBJ] = obj

        status = Status(dict(self._state, **self._op))
        r = self.la.do_analysis(status)
        if r is not None:
            self._result.append(dict(self._op, RESULT=r))

        if id not in self._state.keys():
            self._state[id] = {}
        self._state[id][obj] = (state, self.log.millis)



class Status:
    def __init__(self, state) -> None:
        self._state = state
        self._timers = []

    def state(self, id, obj=''):
        return self._state[id][obj][0]


    def millis(self, id, obj=''):
        return self._state[id][obj][1]


    def op_millis(self):
        return self._state[OP_MILLIS]

    def op_state(self):
        return self._state[OP_STATE]

    def op_id(self):
        return self._state[OP_ID]

    def wait_op_state(self, id, state, timeout, comment):
        self._timers.append((id, state, self._state[OP_MILLIS] + timeout, comment))

    def get_timers(self):
        return self._timers
