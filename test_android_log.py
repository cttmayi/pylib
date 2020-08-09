import conf

from pylib.android.log import log

from pylib.android.log import event_log

# l = log.Log('data/log/main_log_s')
# r = l.find('App')
# print(r)



event = event_log.EventLog('test_data/android/log/events_log')
event_boot = event_log.EventLog('test_data/android/log/events_log.boot')

r_start = event_boot.find(lambda log: log.tag == 'am_proc_start')
r_died = event_boot.find(lambda log: log.tag == 'am_proc_died')

r = event_log.EventLog()
r.merge([event.get_logs(), event_boot.get_logs()], 'index')

print(r.get_logs())

pids = r.get_pids()
for pid in pids:
    print(pid, pids[pid])


