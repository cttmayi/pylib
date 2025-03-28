import os
import sys
# sys.path.append(os.path.join(os.getcwd()))
sys.path.append(os.path.dirname(__file__[0]))

from lparser import LogParser
from lfunc import LogFunc
from lanalysis import LogAnalysis


if __name__ == '__main__':
    la = LogAnalysis()
    # lp:LogParser = LogParser('dataset/simple.log', 'main')
    lp:LogParser = LogParser(sys.argv[1], sys.argv[2])
    logs = lp.get()

    lf = LogFunc(logs, la)
    df = lf.do_func()
    print(df)
