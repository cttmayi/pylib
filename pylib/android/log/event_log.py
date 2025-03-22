
from pylib.android.log import log

import re
import pylib.basic.re_exp.re_exp_ignore as re_exp_ignore

class EventLog(log.Log):
    def __init__(self, path=None):
        log.Log.__init__(self, path)

        if self.logs is not None:
            self.logs['file'] = 'evnet' 



    def _match_pids(self, log):
        pat = None
        if log.tag == 'am_proc_start':
            # am_proc_start: [0,1617,10021,com.android.deskclock,broadcast,com.android.deskclock/.AlarmInitReceiver]
            pat = re_exp_ignore.re_exp(r'[%d,%d,%d,%s,%s,%s/%s]')
        elif log.tag == 'am_proc_died':
            # am_proc_died: [0,1042,com.android.printspooler]
            pat = re_exp_ignore.re_exp(r'[%d,%d,%s]')
        elif log.tag == 'am_kill':
            # am_kill : [0,1078,com.android.provision,15,empty #17]
            pat = re_exp_ignore.re_exp(r'[%d,%d,%s,%d,%s')

        if pat is not None:
            pat = re.compile(pat) 
            m = pat.match(log.msg)
            return m.groups()
        return None


    def _to_value(self, log):
        if log.msg[0] == '[' and log.msg[-1] == ']':
            value = log.msg[1:-1].split(',')
        else:
            value = log.msg
        return value


    def get_pids(self):
        df = self.find(
            lambda log: log.tag == 'am_proc_start' or log.tag == 'am_proc_died' or log.tag == 'am_kill',
            self._to_value
            )

        pids = {}
        for _, log in df.iterrows():
            if log.tag == 'am_proc_start':
                # am_proc_start: [0,1617,10021,com.android.deskclock,broadcast,com.android.deskclock/.AlarmInitReceiver]
                # am_proc_start: [0,18013,10402,com.android.rkpdapp,service,{com.android.rkpdapp/androidx.work.impl.background.systemjob.SystemJobService}, {callerPackage = system, calle
                # print(log.tag_msg)
                pid = log.match[1]
                package = log.match[3]
                time = log.datetime
                reason = log.match[4] + '(' + log.match[5] + ')'
                pids[pid] = { 'pid': pid, 'package': package, 'start_reason': reason, 'start_time': time }
            elif log.tag == 'am_kill':
                # am_kill : [0,1078,com.android.provision,15,empty #17]
                pid = log.match[1]
                package = log.match[2]
                reason = log.match[4]
                if not pid in pids:
                    pids[pid] = { 'pid': pid }
                pids[pid]['package'] = package
                pids[pid]['die_reason'] = reason
            elif log.tag == 'am_proc_died':
                pid = log.match[1]
                package = log.match[2]
                time = log.datetime
                if not pid in pids:
                    pids[pid] = { 'pid': pid }
                pids[pid]['package'] = package
                pids[pid]['die_time'] = time

            # am_proc_died: [0,1042,com.android.printspooler]
        
        return pids



