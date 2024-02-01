import pandas as pd
import os

import utils

from env import *

class LogAnalysis:
    def __init__(self, df):
        self.df:pd.DataFrame = df
        self.init_analysis()

    def init_analysis(self):
        self.func = []
        self.comments = []

        package_name = __name__
        package_path = os.path.dirname(__file__)
        modules = utils.get_modules(package_path)

        for module_name in modules:
            module = utils.import_module(module_name, package_name)
            self.set_analysis(module.get('func'), module.get('comments'))

    def set_analysis(self, func, comments):
        self.func.append(func)
        self.comments.append(comments)

    def _analysis(self, state):
        state = State(state)
        for id in range(len(self.func)):
            ret = None
            if id not in self.func_id:
                try:
                    func = self.func[id]
                    if func is not None:
                        ret = func(state)

                except Exception as e:
                    if str(e) != 'Ignore':
                        print(f'[Error]Analysis func error, id={id}')
                        self.func[id] = None
                if ret is not None:
                    self.func_id.append(id)
                    return ret
        return None

    def analysis(self):
        self.func_id = []
        self.df['result'] = self.df.apply(self._analysis, axis=1)
        return self.df[self.df['result'].notnull()]



