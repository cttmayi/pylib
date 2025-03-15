import pandas as pd
import utils.timestamp as ts

PARSER_FORMAT = ['type', 'date', 'time', 'timestamp', 'pid', 'tid', 'level', 'tag', 'msg']

TIMESTAMP_START = None
# 11-25 19:41:19.813  1153  1153 F libc    : Fatal signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 1153 (init), pid 1153 (init)
def main_parser(lines, type='main'):
    s = pd.Series(lines)
    logs = s.str.split(expand=True, n=5)
    logs.rename(
        columns={0:'date', 1:'time', 2:'pid', 3:'tid', 4:'level', 5:'tag_msg'},
        inplace=True)

    logs.drop(logs[logs.tag_msg.isna()].index, inplace=True) # 删除异常行, 比如第一行"-----timezone: GMT"

    def to_timestamp(log):
        global TIMESTAMP_START
        now = '1970-' + log.date + ' ' + log.time
        now = pd.to_datetime(now, format='%Y-%m-%d %H:%M:%S.%f')
        timestamp = int(ts.ms(now.timestamp()))
        TIMESTAMP_START = TIMESTAMP_START if TIMESTAMP_START is not None else timestamp
        return ts.ms(timestamp - TIMESTAMP_START)
    
    logs['timestamp'] = logs.apply(to_timestamp, axis=1)

    r = logs['tag_msg'].str.split(': ', expand=True, n=1)
    logs['tag'] = r[0].str.strip()
    logs['msg'] = r[1].str.strip()
    logs['type'] = type
    # logs.drop(columns=['tag_msg'], inplace=True)

    # index 重新排列
    logs = logs[PARSER_FORMAT]

    return logs

def debug_parser(lines):
    return main_parser(lines, 'debug')