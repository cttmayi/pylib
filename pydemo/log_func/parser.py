
import numpy as np
import pandas as pd

import pylib.basic.re_exp.re_exp2 as re_exp
from runtime.op import PATTERN_LIST, get_op_func, STATUS_MAP


T = None
# 11-25 19:41:19.813  1153  1153 F libc    : Fatal signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 1153 (init), pid 1153 (init)
def main_parser(lines):
    s = pd.Series(lines)
    logs = s.str.split(expand=True, n=5)
    logs.rename(
        columns={0:'date', 1:'time', 2:'pid', 3:'tid', 4:'level', 5:'tag_msg'},
        inplace=True)

    logs.drop(logs[logs.tag_msg.isna()].index, inplace=True) # 删除异常行, 比如第一行"-----timezone: GMT"

    # logs['datetime'] = logs['date'] + ' ' + logs['time']
    # logs['datetime'] = pd.to_datetime(logs['datetime'], format='%m-%d %H:%M:%S.%f')

    def to_timestamp(log):
        global T
        now = '1970-' + log.date + ' ' + log.time
        now = pd.to_datetime(now, format='%Y-%m-%d %H:%M:%S.%f')
        millis = int(now.timestamp() * 1000)
        T = T if T is not None else millis
        return millis - T
    
    logs['millis'] = logs.apply(to_timestamp, axis=1)

    r = logs['tag_msg'].str.split(': ', expand=True, n=1)
    logs['tag'] = r[0].str.strip()
    logs['msg'] = r[1].str[:-1]
    return logs


class LogParser():
    def __init__(self, path, type=None):
        self.logs:pd.DataFrame = None
        self.op_result = []
        self.status_map = STATUS_MAP
        self.init_parser()

        with open(path, errors='ignore') as fp:
            lines = fp.readlines()
            parser = self._parser[type]
            self.logs = parser(lines)

    def init_parser(self):
        self.matcher = re_exp.FormatMatcher(PATTERN_LIST)

        self._parser = {
            'main': main_parser
        }

    def transfor_to_df(self, ffilter=None):
        if ffilter is None:
            logs = self.logs.copy()
        else:
            logs = self.logs[self.logs.apply(ffilter, axis=1)]
        return logs


    def _op_transfer(self, log):
        r = self.matcher.match(log.msg)
        if r is not None:
            self.op_result.append({'op': r[0], 'args': r[1], 'millis': log.millis, 'line_number': log.name})

    def transfor_to_op(self, log_df):
        log_df.apply(self._op_transfer, axis=1)
        df = pd.DataFrame(self.op_result)
        return df

    def op_execute(self, op_df):
        errors = []
        
        for _, row in op_df.iterrows():
            
            for status in self.status_map.values():
                status.set_current_info(row['millis'], row['line_number'])
            op = row['op']
            args = row['args']
            for op_func in get_op_func(op):
                error = op_func(**args)
                if error is not None:
                    errors.extend(error)
        return errors
        


    # def merge(self, logs, sort='datetime'):
    #     if self.logs is not None:
    #         self.logs = pd.concat([ self.logs, *logs ])
    #     else:
    #         self.logs = pd.concat([ *logs ])

    #     self.logs.drop_duplicates(inplace=True)
    #     if sort == 'index':
    #         self.logs.sort_index(ascending=True, inplace=True)
    #     elif sort is not None:
    #         self.logs.sort_values(by=sort, ascending=True, inplace=True)
        


