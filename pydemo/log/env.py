import pandas as pd

l_status = {}
l_status_once = {}

_l_status_internal = {}


def status_set(id, status):
    l_status[id] = status

def status_inc(id, inc):
    if id in l_status.keys():
        l_status[id] += inc
    else:
        l_status[id] = inc

def status_freq(id, time):
    now = pd.to_datetime('2023-' + time)
    millis:pd.Timestamp = now.timestamp() * 1000
    
    if id in _l_status_internal.keys():
        millis_ = _l_status_internal[id]
        l_status[id] = millis - millis_

    _l_status_internal[id] = millis