import utils.env


from parser import LogParser
#from lfunc import LogFunc
#from lanalysis import LogAnalysis


if __name__ == '__main__':
    # la = LogAnalysis()
    lp:LogParser = LogParser('log/simple.log', 'main')
    # lp:LogParser = LogParser(sys.argv[1], sys.argv[2])
    logs = lp.transfor_to_df()
    print(logs)
    print('------------------------')
    ops = lp.transfor_to_op(logs)
    errors = lp.op_execute(ops)

    for error in errors:
        print(error.get_error_msg(logs))
    # print(ops)
    #lf = LogFunc(logs, la)
    #df = lf.do_func()
    #print(df)