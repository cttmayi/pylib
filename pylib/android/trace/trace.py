


# https://limboy.me/t/chrome-trace-viewer/30

# https://github.com/catapult-project/catapult/blob/master/tracing/tracing/base/color_scheme.html

# https://github.com/catapult-project/catapult/tree/master/tracing/tracing_build

# {
#   "name": "myName", // 事件名，会展示在 timeline 上
#   "cat": "category,list", // 事件分类，类似 Tag，但 UI 上不支持选择 Tag
#   "ph": "B", // phase，后面着重会讲到
#   "ts": 12345, // 事件发生时的时间戳，以微秒表示
#   "pid": 123, // 进程名
#   "tid": 456, // 线程名
#   "args": { // 额外参数，当选中某个 event 后，会在底部的面板展示
#     "someArg": 1,
#     "anotherArg": {
#       "value": "my value"
#     }
#   }
# }

# ph B/E // 正常的开始/结束事件，最常见，也可以用 X + dur 来表示
# ph M // Metadata 用来对一类 Event 附加更详细的信息，可以带来 UI 上的变化
# ph I // 瞬时事件，类似 Mark 一下
# ph s/e // 异步事件，表示自定义的一个事件，表现上跟正常事件会有区别
# ph s/f // Flow 事件，会出现箭头，要通过 ts 匹配最近的 event，结束要使用 bp: e
# ph O // Snapshot，表现上是一个醒目的圆点，可以在 `args.snapshot` 里放任意数据

import json

def _new(task, sub_task, event, phase, ts, more=None, cat=None, args=None):
    ret = {}
    ret['pid'] = task
    ret['tid'] = sub_task
    ret['name'] = event # 事件名
    if cat is not None:
        ret['cat'] = cat
    ret['ph'] = phase
    ret['ts'] = ts

    if more is not None:
        for key in more:
            ret[key] = more[key]

    if args is not None:
        ret['args'] = args

    return ret


def to_file(data, path):
    f = open(path,'w',encoding='utf-8')
    json.dump(data, f, ensure_ascii=False)
    f.close()


def load_file(path):
    f = open(path,'r',encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


class Trace():
    def __init__(self):
        self.events = []
        pass

    def new_event(self, task, sub_task, event):
        event = Event(task, sub_task, event)
        event.set_trace(self)
        return event

    
    def append(self, event):
        self.events.append(event)


    def save(self, path):
        to_file(self.events, path)


class Event():
    def __init__(self, task, sub_task, event):
        self.task = task
        self.sub_task = sub_task
        self.event = event
        
        self.trace = None

    
    def set_trace(self, trace):
        self.trace = trace


    def begin(self, ts):
        e = _new(self.task, self.sub_task, self.event, 'B', ts)
        if self.trace is not None:
            self.trace.append(e)
        return e


    def end(self, ts):
        e = _new(self.task, self.sub_task, self.event, 'E', ts)
        if self.trace is not None:
            self.trace.append(e)
        return e


    def dur(self, ts, dur):
        e = _new(self.task, self.sub_task, self.event, 'X', ts, more={'dur': dur})
        if self.trace is not None:
            self.trace.append(e)
        return e


if __name__ == '__main__':
    t = Trace()
    e1 = t.new_event('T1', 'TS1', 'E1')
    e2 = t.new_event('T1', 'TS2', 'E2')
    e3 = t.new_event('T2', 'TS3', 'E3')

    e1.begin(0)
    e1.end(100)

    e1.begin(300)
    e1.end(500)

    e2.begin(1000)
    e2.end(1100)

    e3.begin(1200)
    e3.end(1300)

    e1.dur(1200, 300)


    t.save('output')

