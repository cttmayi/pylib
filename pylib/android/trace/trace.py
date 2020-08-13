
# https://limboy.me/t/chrome-trace-viewer/30

# https://github.com/catapult-project/catapult/tree/master/tracing/tracing_build

# ph B/E // 正常的开始/结束事件，最常见，也可以用 X + dur 来表示
# ph M // Metadata 用来对一类 Event 附加更详细的信息，可以带来 UI 上的变化
# ph I // 瞬时事件，类似 Mark 一下
# ph s/e // 异步事件，表示自定义的一个事件，表现上跟正常事件会有区别
# ph s/f // Flow 事件，会出现箭头，要通过 ts 匹配最近的 event，结束要使用 bp: e
# ph O // Snapshot，表现上是一个醒目的圆点，可以在 `args.snapshot` 里放任意数据

import json

def _new(task, sub_task, event, phase, ts, more=None, color=None, cat=None, args=None):
    ret = {}
    ret['pid'] = task
    if sub_task is not None:
        ret['tid'] = sub_task
    ret['name'] = event # 事件名
    if cat is not None:
        ret['cat'] = cat
    ret['ph'] = phase
    ret['ts'] = ts

    if color is not None:
        ret['cname'] = color

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
        self.traces = []
        self.events = {}
        pass

    def get_event(self, name, task='default', sub_task=None):
        if name in self.events:
            event = self.events[name]
        else:
            event = Event(name, task, sub_task)
            event.set_trace(self)
            self.events[name] = event
        return event

    
    def append(self, event):
        self.traces.append(event)


    def save(self, path):
        to_file(self.traces, path)


class Event():
    def __init__(self, name, task='default', sub_task=None):
        self.task = task
        self.sub_task = sub_task
        self.name = name

        self.color = None
        
        self.trace = None

    
    def set_trace(self, trace):
        self.trace = trace

    # good: new tr.b.Color(0, 125, 0),
    # bad: new tr.b.Color(180, 125, 0),
    # terrible: new tr.b.Color(180, 0, 0),

    # black: new tr.b.Color(0, 0, 0),
    # grey: new tr.b.Color(221, 221, 221),
    # white: new tr.b.Color(255, 255, 255),
    # yellow: new tr.b.Color(255, 255, 0),
    # olive: new tr.b.Color(100, 100, 0),
    # # https://github.com/catapult-project/catapult/blob/master/tracing/tracing/base/color_scheme.html
    def set_color(self, color):
        self.color = color


    def _default_task(self, task, sub_task):
        if task is None:
            task = self.task
            if sub_task is None:
                sub_task = self.sub_task

        if sub_task is None:
            sub_task = task

        return task, sub_task


    def begin(self, ts, task=None, sub_task=None, args=None):
        task, sub_task = self._default_task(task, sub_task)

        e = _new(task, sub_task, self.name, 'B', ts, args=args)
        if self.trace is not None:
            self.trace.append(e)
        return e


    def end(self, ts, task=None, sub_task=None):
        task, sub_task = self._default_task(task, sub_task)

        e = _new(task, sub_task, self.name, 'E', ts, color=self.color)
        if self.trace is not None:
            self.trace.append(e)
        return e


    def dur(self, ts, dur=0, task=None, sub_task=None, args=None):
        task, sub_task = self._default_task(task, sub_task)

        if dur != 0:
            e = _new(task, sub_task, self.name, 'X', ts, color=self.color, more={'dur': dur}, args=args)
        else:
            e = _new(task, sub_task, self.name, 'I', ts, color=self.color, args=args) 
        if self.trace is not None:
            self.trace.append(e)
        return e


    def snapshot(self, ts, task=None):
        task, _ = self._default_task(task, None)

        e = _new(task, None, self.name, 'O', ts, more={'id': self.name}, args={"snapshot": self.name}, color=self.color) 
        if self.trace is not None:
            self.trace.append(e)
        return e


if __name__ == '__main__': # for test
    t = Trace()
    e1 = t.get_event('E1','T1')
    e2 = t.get_event('E2', 'T1', 'T2')
    e2.set_color('yellow')

    e3 = t.get_event('E3', 'T2')
    s3 = t.get_event('S3', 'T3')
    i3 = t.get_event('I3', 'T3')

    s3.snapshot(40)

    i3.dur(50)

    e1.begin(0)
    e1.end(100)

    s3.snapshot(120)

    s3.snapshot(180, 'T2')

    s3.snapshot(210, 'T2')

    e1.begin(10)
    e1.end(50)

    e1.begin(300, 'T2')
    e1.end(500, 'T2')

    e2.begin(1000)
    e2.end(1100)

    e3.begin(1200)
    e3.end(1300)

    e1.dur(1200, 300)

    t.save('test_output')

