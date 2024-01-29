
import pandas as pd

from pprint import pprint as print

from env import l_status, l_status_once

import utils
import os

class LogFunc:
    def __init__(self, df, tags = None):
        self.df:pd.DataFrame = df
        self.logs_record = []
        self.init_func(tags)

    def init_func(self, tags):
        self.tag_func = {}

        package_name = __name__
        package_path = os.path.dirname(__file__)
        modules = utils.get_modules(package_path)

        for module_name in modules:
            if tags is None or module_name in tags:
                module = utils.import_module(module_name, package_name)
                self.set_func(module_name, module.get('func'))

    def set_func(self, tag, func):
        self.tag_func[tag] = func

    def _func(self, log):
        if log.tag in self.tag_func.keys():
            l_status_once = {}
            func = self.tag_func[log.tag]
            func(log)
            status = dict(l_status, **l_status_once)
            self.logs_record.append(status)

    def func(self):
        self.df.apply(self._func, axis=1)
        df = pd.DataFrame(self.logs_record)
        return df




    

