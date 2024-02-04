
OP_ID = '_OP_ID'
OP_OBJ = '_OP_OBJ'
OP_STATE = '_OP_STATE'
OP_MILLIS = '_OP_MILLIS'
TIME  = '_TIME'

class Env:
    def __init__(self):
        self._state = {}
        self._op = {}

    def get_status(self):
        return self._status

    def reset(self, log):
        self._status = []
        self._op = {}
        self.log = log
        self._op[TIME] = log.time

    def state_set(self, id, state, obj=None):
        self._op[OP_ID] = id
        self._op[OP_STATE] = state
        self._op[OP_MILLIS] = self.log.millis
        if obj is not None:
            self._op[OP_OBJ] = obj
        self._status.append(dict(self._state, **self._op))

        if obj is not None:
            if id not in self._state.keys():
                self._state[id] = {}
            self._state[id][obj] = (state, self.log.millis)
        else:
            self._state[id] = (state, self.log.millis)



class Status:
    def __init__(self, state) -> None:
        self._state = state
        self._timers = []

    def state(self, id, obj=None):
        if obj is not None:
            return self._state[id][obj]
        else:
            return self._state[id][0]

    def millis(self, id, obj=None):
        if obj is not None:
            return self._state[id][obj]
        else:
            return self._state[id][1]

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
