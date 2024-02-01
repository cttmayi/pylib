import pandas as pd


T = None

# 11-25 19:41:19.813  1153  1153 F libc    : Fatal signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 1153 (init), pid 1153 (init)
def parser(lines):
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