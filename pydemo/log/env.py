import pandas as pd

l_status = {}
l_status_temp = {}


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
    
    if id in l_status_temp.keys():
        millis_ = l_status_temp[id]
        l_status[id] = millis - millis_

    l_status_temp[id] = millis