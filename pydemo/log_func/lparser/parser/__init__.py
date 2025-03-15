import pandas as pd
import logging
import re
import pylib.basic.re_exp.re_exp2 as re_exp
from runtime.op import PATTERN_LIST, STATUS_MAP, get_op_func, get_op_name, get_op_func_init
from lparser.parser.android import main_parser, debug_parser, PAESER_MAIN_REGEX

PARSER_FORMAT = ['type', 'date', 'time', 'timestamp', 'pid', 'tid', 'level', 'tag', 'msg']


PARSER_MAP = {
    'debug': (debug_parser, PAESER_MAIN_REGEX),
    'main':  (main_parser, PAESER_MAIN_REGEX),
}

class LogParser():
    def __init__(self, path, type=None, looper=None):
        self.path = path
        self.type = type
        self.logs:pd.DataFrame = None
        self.op_result = []
        self.status_list = STATUS_MAP.keys()
        self.matcher = re_exp.FormatMatcher(PATTERN_LIST)
        self._parser = { k: p[0] for k, p in PARSER_MAP.items() }
        self._parser_regex = { k: p[1] for k, p in PARSER_MAP.items() }
        self.looper = looper



    def auto_detect_type(self, lines):
        for k in self._parser_regex:
            regex = re.compile(self._parser_regex[k])
            count = 0
            for i in range(100):
                if i >= len(lines): break
                if regex.match(lines[i]):
                    count += 1
                    if count >= 10:
                        return k
        return None

    def transfor_to_df(self, ffilter=None):
        with open(self.path, errors='ignore') as fp:
            lines = fp.readlines()
            lines = [l.strip() for l in lines] # remove \n

        type = self.type
        if type is None:
            type = self.auto_detect_type(lines)

        if type is None:
            logging.error('can not detect log type')
        else:
            logging.info('log type: {}'.format(type))
            parser = self._parser[type]
            self.logs = parser(lines)

            if ffilter is None:
                logs = self.logs.copy()
            else:
                logs = self.logs[self.logs.apply(ffilter, axis=1)]
            return logs
        return None

    def _op_transfer(self, log):
        r = self.matcher.match(log.msg)

        if r is not None:
            type = log.type
            line = log.name
            timestamp = log.timestamp
            name = get_op_name(type, r[0])
            op = r[0]
            args = r[1]
            tid = log.tid

            op_f = {'type': type, 'line': line, 'timestamp': timestamp, 'tid': tid,  'name': name, 'op': op, 'args': args, 'n': 1}

            # 通过op_by_tid来缓存的op_f， 延迟放入op_result
            op_f_last = self.op_by_tid.get(tid)
            if op_f_last is not None and op_f_last['name'] == name and op_f_last['op'] != op:
                    new_args = {}
                    for k in args:
                        new_args[k + '_' + str(op_f_last['n'])] = args[k]
                    op_f_last['args'].update(new_args)
                    op_f_last['n'] += 1
            else:
                self.op_by_tid[tid] = op_f
                self.op_result.append(op_f)            

    def transfor_to_op(self, log_df:pd.DataFrame):
        self.op_by_tid = {}
        self.op_result = []
        log_df.apply(self._op_transfer, axis=1)
        df = pd.DataFrame(self.op_result)
        return df

    def op_execute(self, op_df: pd.DataFrame):
        execute_method = self.op_execute_looper if self.looper is not None else self.op_execute_runtime
        return execute_method(op_df)

    def op_execute_looper(self, op_df:pd.DataFrame):
        logging.debug('====== op_execute looper ======')
        for _, row in op_df.iterrows():
            op = row['op']
            name = row['name']
            args = row['args']
            type = row['type']
            line = row['line']
            timestamp = row['timestamp']
            self.looper(name, args, timestamp, line)

    def op_execute_runtime(self, op_df:pd.DataFrame):
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

        logging.debug('====== op_execute func ======')
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
        


