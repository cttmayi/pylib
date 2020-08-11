import conf
import re

from pylib.android.log import log
from pylib.android.log import event_log
from pylib.android.trace import trace

def _to_value(log):
    if log.msg[0] == '[' and log.msg[-1] == ']':
        value = log.msg[1:-1].split(',')
    else:
        value = log.msg
    return value


def str2time(time_str):
    m = re.match('(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3,6})', time_str)
    return (((((int(m.group(1))-1) * 31 + (int(m.group(2)))-1) * 24 + int(m.group(3))) * 60 + int(m.group(4))) * 60 + int(m.group(5))) * 1000000 + int(m.group(6))


event_boot = event_log.EventLog('test_data/android/log/events_log')
r = event_boot.find(lambda log: log.tag == 'am_proc_start' or log.tag == 'am_proc_died', _to_value)

t = trace.Trace()
time_start = None
for _, log in r.iterrows():
    if log.tag == 'am_proc_start':
        # am_proc_start: [0,1617,10021,com.android.deskclock,broadcast,com.android.deskclock/.AlarmInitReceiver]
        pid = log.match[1]
        package = log.match[3]
        time = str2time(log.datetime)
        reason = log.match[4] + '(' + log.match[5] + ')'

        if time_start is None:
            time_start = time

        e = t.new_event(package, pid, package)
        e.begin(time - time_start)
        print('am_proc_start', package)

    elif log.tag == 'am_proc_died':
        pid = log.match[1]
        package = log.match[2]
        time = str2time(log.datetime)

        if time_start is None:
            time_start = time

        e = t.new_event(package, pid, package)
        e.end(time - time_start)
        print('am_proc_died', package)


t.save('test_output')




