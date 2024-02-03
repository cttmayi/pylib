import pandas as pd
import os

import utils
import traceback

from env import Status

class LogAnalysis:
    def __init__(self, df):
        self.df:pd.DataFrame = df
        self.init_analysis()

        self._timers = []

    def init_analysis(self):
        self.func = {}

        package_name = __name__
        package_path = os.path.dirname(__file__)
        modules = utils.get_modules(package_path)

        for module_name in modules:
            func = utils.import_module(module_name, package_name)

            analysis_func = []
            for f in func.keys():
                if f.startswith('func_'):
                    analysis_func.append(func.get(f))

            self.set_analysis(module_name, analysis_func)

    def set_analysis(self, id, func):
        self.func[id] = func

    def _analysis(self, status):
        obj_status = Status(status)
        key = obj_status.op_id()
        ret = []
        if key in self.func.keys():
            try:
                funcs = self.func[key]
                for func in funcs:
                    r = func(obj_status)
                    if r is not None:
                        ret.append(r)

                timers = []
                for sid in range(len(self._timers)):
                    id, state, timeout, comment = self._timers[sid]
                    # print('Timer', obj_status.op_millis(), sid, state, timeout, comment)
                    if timeout < obj_status.op_millis():
                        ret.append(comment)
                    elif id == obj_status.op_id() and state == obj_status.op_state():
                        pass
                    else:
                        timers.append(self._timers[sid])

                self._timers = timers
                self._timers.extend(obj_status.get_timers())
            
            except KeyError as e:
                # print(e.__class__.__name__)
                # print(traceback.print_exc())
                pass
            except TypeError as e:
                pass
            except Exception as e:
                # print(e.__class__.__name__, e)
                print(f'[Error]Analysis func error, id={key}')
                print(traceback.print_exc())
                del self.func[key]

        return ret if len(ret) > 0 else None

    def analysis(self):
        self.df['result'] = self.df.apply(self._analysis, axis=1)
        return self.df[self.df['result'].notnull()]



