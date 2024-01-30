
import numpy as np
import pandas as pd

import os
import utils

class LogParser():
    def __init__(self, path, type=None):
        self.logs:pd.DataFrame = None

        self.init_parser()

        with open(path, errors='ignore') as fp:
            lines = fp.readlines()
            parser = self._parser[type]
            self.logs = parser(lines)

    def init_parser(self):
        self._parser = {}

        package_name = __name__
        package_path = os.path.dirname(__file__)
        modules = utils.get_modules(package_path)

        for module_name in modules:
            module = utils.import_module(module_name, package_name)
            self.set_parser(module_name, module.get('parser'))

    def set_parser(self, type, func):
        self._parser[type] = func

    def get(self, ffilter=None):
        if ffilter is None:
            logs = self.logs.copy()
        else:
            logs = self.logs[self.logs.apply(ffilter, axis=1)]
        return logs

    def merge(self, logs, sort='datetime'):
        if self.logs is not None:
            self.logs = pd.concat([ self.logs, *logs ])
        else:
            self.logs = pd.concat([ *logs ])

        self.logs.drop_duplicates(inplace=True)
        if sort == 'index':
            self.logs.sort_index(ascending=True, inplace=True)
        elif sort is not None:
            self.logs.sort_values(by=sort, ascending=True, inplace=True)
        


