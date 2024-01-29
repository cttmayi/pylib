
import numpy as np
import pandas as pd

from datetime import datetime


class LogParser():
    def __init__(self, path, type='android'):
        self.logs:pd.DataFrame = None

        with open(path, errors='ignore') as fp:
            lines = fp.readlines()
            if type == 'android':
                self.logs = self._parser_android(lines)


    def _parser_android(self, lines):
        s = pd.Series(lines)
        logs = s.str.split(expand=True, n=5)
        logs.rename(
            columns={0:'date', 1:'time', 2:'pid', 3:'tid', 4:'level', 5:'tag_msg'},
            inplace=True)

        logs.drop(logs[logs.tag_msg.isna()].index, inplace=True) # 删除异常行, 比如第一行"-----timezone: GMT"

        logs['datetime'] = logs['date'] + ' ' + logs['time']
        r = logs['tag_msg'].str.split(': ', expand=True, n=1)
        logs['tag'] = r[0].str.strip()
        logs['msg'] = r[1].str[:-1]
        return logs


    def get(self, ffilter=None):
        if ffilter is None:
            logs = self.logs.copy()
        else:
            logs = self.logs[self.logs.apply(ffilter, axis=1)]
        return logs

    def merge(self, logs, sort='datetime'):
        if self.logs is not None:
            self.logs = pd.concat([ self.logs, *logs ])
        else:
            self.logs = pd.concat([ *logs ])

        self.logs.drop_duplicates(inplace=True)
        if sort == 'index':
            self.logs.sort_index(ascending=True, inplace=True)
        elif sort is not None:
            self.logs.sort_values(by=sort, ascending=True, inplace=True)
        


