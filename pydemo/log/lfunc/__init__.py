
import pandas as pd

from pprint import pprint as print

from lenv import Env

import utils
import os

class LogFunc:
    def __init__(self, df, la, tags = None):
        self.df:pd.DataFrame = df
        self.result = []
        self.init_func(tags)
        self.env:Env = Env(la)

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
            self.env.reset(log)
            func = self.tag_func[log.tag]
            func(self.env, log)
            status = self.env.get_result()
            self.result.extend(status)

    def do_func(self):
        self.df.apply(self._func, axis=1)
        df = pd.DataFrame(self.result)
        return df




    

