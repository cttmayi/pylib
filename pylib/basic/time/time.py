from datetime import datetime

ONE_MINUTE = 60
ONE_HOUR = 60 * 60
ONE_DAY = 60 * 60 * 24


def DAY(df):
    return int(df/ONE_DAY)


def HOUR(df):
    return int(df/ONE_HOUR)


def MINUTE(df):
    return int(df/ONE_MINUTE)


def get_now():
    day = datetime.now()
    return day


def get_esdate(day=None):
    if day is None:
        day = datetime.now()
    return day.strftime('%Y-%m-%dT%H:%M:%S+0800')


def get_estimestamp(day=None):
    return int(get_timestamp(day))


def get_timestamp(day=None):
    if day is None:
        day = datetime.now()
    return day.timestamp()


def get_time_df(tst1, tst2=None, unit=DAY):
    if tst2 is None:
        tst2 = get_timestamp()
    tdf = tst2 - tst1
    return unit(tdf)


if __name__ == '__main__':
    print(get_esdate())
    print(get_estimestamp())
    print(get_timestamp())
    print(get_time_df(0))