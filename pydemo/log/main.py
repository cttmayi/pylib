import os
import sys
# sys.path.append(os.path.join(os.getcwd()))
sys.path.append(os.path.dirname(__file__[0]))

import pandas as pd

# import pylib.android.log.log as log
from log import LogParser
from func import LogFunc
from analysis import LogAnalysis

if __name__ == '__main__':
    lp:LogParser = LogParser('dataset/android_event.log')
    logs = lp.get()

    lf = LogFunc(logs)

    df = lf.func()

    la = LogAnalysis(df)
    r = la.analysis()
    print(r)






