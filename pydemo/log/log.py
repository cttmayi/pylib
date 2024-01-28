
import numpy as np
import pandas as pd

from datetime import datetime


class LogParser():
    def __init__(self, path=None):
        self.logs:pd.DataFrame = None
        if path is not None:
            with open(path) as fp:
                lines = fp.readlines()
                s = pd.Series(lines)
                self.logs = s.str.split(expand=True, n=5)
                self.logs.rename(
                    columns={0:'date', 1:'time', 2:'pid', 3:'tid', 4:'level', 5:'tag_msg'},
                    inplace=True)

                self.logs.drop(self.logs[self.logs.tag_msg.isna()].index, inplace=True) # 删除异常行, 比如第一行"-----timezone: GMT"

                self.logs['datetime'] = self.logs['date'] + ' ' + self.logs['time']
                r = self.logs['tag_msg'].str.split(': ', expand=True, n=1)
                self.logs['tag'] = r[0].str.strip()
                self.logs['msg'] = r[1].str[:-1]


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
        


