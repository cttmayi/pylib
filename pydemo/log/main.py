import os
import sys
# sys.path.append(os.path.join(os.getcwd()))
sys.path.append(os.path.dirname(__file__[0]))

from lparser import LogParser
from lfunc import LogFunc
from lanalysis import LogAnalysis


if __name__ == '__main__':
    lp:LogParser = LogParser('dataset/simple.log', 'main')
    logs = lp.get()

    lf = LogFunc(logs)

    df = lf.func()
    print(df)

    la = LogAnalysis(df)
    r = la.analysis()
    print(r)
