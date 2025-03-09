import pandas as pd
import pylib.basic.re_exp.re_exp2 as re_exp
from runtime.op import PATTERN_LIST, STATUS_MAP, STATUS_GLOBAL, get_op_func, get_op_name, get_op_func_init
import logging

PARSER_FORMAT = ['type', 'date', 'time', 'timestamp', 'pid', 'tid', 'level', 'tag', 'msg']

from parser.android import main_parser as main_parser
PARSER_MAP = {
    'main':  main_parser,
}

class LogParser():
    def __init__(self, path, type=None):
        self.logs:pd.DataFrame = None
        self.op_result = []
        self.status_list = [STATUS_GLOBAL]
        self.status_list.extend(STATUS_MAP.values())
        self.matcher = re_exp.FormatMatcher(PATTERN_LIST)
        self._parser = PARSER_MAP

        with open(path, errors='ignore') as fp:
            lines = fp.readlines()
            lines = [l.strip() for l in lines]
            parser = self._parser[type]
            self.logs = parser(lines)

    def transfor_to_df(self, ffilter=None):
        if ffilter is None:
            logs = self.logs.copy()
        else:
            logs = self.logs[self.logs.apply(ffilter, axis=1)]
        return logs

    def _op_transfer(self, log):
        r = self.matcher.match(log.msg)
        if r is not None:
            type = log.type
            name = get_op_name(type, r[0])
            self.op_result.append({'type': type, 'line': log.name, 'timestamp': log.timestamp, 'name': name, 'op': r[0], 'args': r[1], })

    def transfor_to_op(self, log_df):
        log_df.apply(self._op_transfer, axis=1)
        df = pd.DataFrame(self.op_result)
        return df

    def op_execute(self, op_df:pd.DataFrame):
        logging.debug('====== op_execute init ======')
        for _, row in op_df.iterrows():
            for status in self.status_list:
                status.set_current_info(row['timestamp'], row['line'])
            op = row['op']
            args = row['args']
            type = row['type']

            func_inits = get_op_func_init(type, op)
            if func_inits is not None and len(func_inits) > 0:
                for status in self.status_list:
                    logging.debug('status: %s', status.get_all_status())
                logging.debug('\top %s', row.to_dict())
                for op_func in func_inits:
                    op_func(**args)

        logging.debug('====== op_execute ======')
        errors = []
        for _, row in op_df.iterrows():
            op = row['op']
            args = row['args']
            type = row['type']
            line = row['line']
            timestamp = row['timestamp']
            for status in self.status_list:
                status.set_current_info(timestamp, line)

            funcs = get_op_func(type, op)
            if funcs is not None and len(funcs) > 0:
                for status in self.status_list:
                    logging.debug('status: %s', status.get_all_status())
                logging.debug('\top: %s', row.to_dict())
                for op_func in funcs:
                    op_func(**args)
        
        for status in self.status_list:
            status.end_checker()
            error = status.get_error()
            errors.extend(error)
            status.reset_error()

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
        


