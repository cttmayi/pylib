
# https://github.com/catapult-project/catapult/tree/master/tracing/tracing_build

# ph B/E // 正常的开始/结束事件，最常见，也可以用 X + dur 来表示
# ph M // Metadata 用来对一类 Event 附加更详细的信息，可以带来 UI 上的变化
# ph I // 瞬时事件，类似 Mark 一下
# ph s/e // 异步事件，表示自定义的一个事件，表现上跟正常事件会有区别
# ph s/f // Flow 事件，会出现箭头，要通过 ts 匹配最近的 event，结束要使用 bp: e
# ph O // Snapshot，表现上是一个醒目的圆点，可以在 `args.snapshot` 里放任意数据
# ph C // Counter Events

    # "stackFrames":
    # {
    #     "5": { "name": "F_A" },
    #     "7": { "name": "F_B", "parent": "5" },
    #     "9": { "name": "F_C", "parent": "5" }
    # }

# cname
    # good: new tr.b.Color(0, 125, 0),
    # bad: new tr.b.Color(180, 125, 0),
    # terrible: new tr.b.Color(180, 0, 0),

    # black: new tr.b.Color(0, 0, 0),
    # grey: new tr.b.Color(221, 221, 221),
    # white: new tr.b.Color(255, 255, 255),
    # yellow: new tr.b.Color(255, 255, 0),
    # olive: new tr.b.Color(100, 100, 0),
    # # https://github.com/catapult-project/catapult/blob/master/tracing/tracing/base/color_scheme.html



debug = True


import json

def _new(pid, tid, name, phase, ts, more=None, args=None, default=None):
    ret = {}
    ret['pid'] = pid
    if tid is not None:
        ret['tid'] = tid
    if name is not None:
        ret['name'] = name # 事件名

    ret['ph'] = phase
    ret['ts'] = ts

    if more is not None:
        for key in more:
            ret[key] = more[key]

    if args is not None:
        ret['args'] = args

    if default is not None:
        color = default.get('color', None)
        if color is not None:
            ret['cname'] = color
        category = default.get('category', None)    
        if category is not None:
            ret['cat'] = category

    return ret


def _to_file(data, path):
    f = open(path,'w', encoding='utf-8')
    if debug:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ':'))
    else:
        json.dump(data, f, ensure_ascii=False)
    f.close()


def _load_file(path):
    f = open(path,'r', encoding='utf-8', errors='ignore')
    data = json.load(f)
    f.close()
    return data


class Trace():
    def __init__(self, time_unit='ms', ending=False):
        self.traces = []
        self.flows = set()
        self.display_time_unit = time_unit

        self.ending = ending
        self.ends = {}
        self.endtime = 0

    _PROCESS = 'process_name'
    _THREAD = 'thread_name'

    def set_metadata_process(self, pid, name):
        e = _new(pid, 0, self._PROCESS, 'M', 0, args={'name': name})
        self.traces.append(e)


    def set_metadata_thread(self, pid, tid, name):
        e = _new(pid, tid, self._THREAD, 'M', 0, args={'name': name})
        self.traces.append(e)


    def _end(self, pid, tid, value=1):
        if pid not in self.ends:
            self.ends[pid] = {}
        if tid not in self.ends[pid]:
            self.ends[pid][tid] = 0
        
        if self.ends[pid][tid] + value > 0:
            self.ends[pid][tid] = self.ends[pid][tid] + value
        else:
            self.ends[pid][tid] = 0



    def begin(self, name, pid, tid, ts, args=None, default=None):
        e = _new(pid, tid, name, 'B', ts, args=args, default=default)
        self.traces.append(e)

        if self.ending:
            self._end(pid, tid, 1)
            if self.endtime < ts:
                self.endtime = ts


    def end(self, pid, tid, ts, default=None):
        e = _new(pid, tid, None, 'E', ts, default=default)
        self.traces.append(e)

        if self.ending:
            self._end(pid, tid, -1)
            if self.endtime < ts:
                self.endtime = ts

    def dur(self, name, pid, tid, ts, dur=0, bind_id=None, args=None, default=None):
        if dur != 0:
            if bind_id is None:
                e = _new(pid, tid, name, 'X', ts, more={'dur': dur}, args=args, default=default)
            else:
                if bind_id in self.flows:
                    e = _new(pid, tid, name, 'X', ts, 
                        more={'dur': dur, 'bind_id': bind_id, "flow_in":True,"flow_out":True},
                        args=args,
                        default=default
                    )
                else:
                    self.flows.add(bind_id)
                    e = _new(pid, tid, name, 'X', ts, 
                        more={'dur': dur, 'bind_id': bind_id, "flow_out":True},
                        args=args,
                        default=default
                    )
        else:
            e = _new(pid, tid, name, 'I', ts, args=args, default=default) 
        self.traces.append(e)

        if self.ending:
            if self.endtime < ts + dur:
                self.endtime = ts + dur


    def snapshot(self, name, pid, ts, default=None):
        e = _new(pid, None, name, 'O', ts, more={'id': name, 'cat': 'cat'}, args={"snapshot": {'cat': name}}, default=default) 
        self.traces.append(e)


    def counter(self, name, pid, ts, args, default=None):
        e = _new(pid, None, name, 'C', ts, args=args, default=default)
        self.traces.append(e)


    def scheduler_running(self, pid, tid, ts, cpu):
        e = _new(pid, tid, 'Scheduler', 'S', ts, more={'id2': {'local': cpu}, 'cat': 'CPU'}, args={'name': 'Running'}) 
        self.traces.append(e)

    def scheduler_sleep(self, pid, tid, ts, cpu):
        e = _new(pid, tid, 'Scheduler', 'F', ts, more={'id2': {'local': cpu}, 'cat': 'CPU'})
        self.traces.append(e)


    # state = STATE_DROPPED
    # def frame_begin(self, name, pid, tid, ts, id, state=''):
    #     e = _new(pid, tid, name, 'b', ts,
    #         args={"chrome_frame_reporter":{"frame_sequence":id, "frame_source":0, "state":state}},
    #         more={'id': '0x1000', 'cat': 'Frame'},
    #     )
    #     self.traces.append(e)
        

    # def frame_end(self, name, pid, tid, ts):
    #     e = _new(pid, tid, name, 'e', ts,
    #         more={'id': '0x1000', 'cat': 'Frame'},
    #     )
    #     self.traces.append(e)


    def save(self, path):
        for pid in self.ends:
            for tid in self.ends[pid]:
                for _ in range(self.ends[pid][tid]):
                    self.end(pid, tid, self.endtime)

        out = {
            'traceEvents': self.traces,
            'displayTimeUnit': self.display_time_unit,
        }
        _to_file(out, path)


# chrome://tracing/
if __name__ == '__main__': # for test
    t = Trace(ending=True)

    pid_main = 100
    tid_main = 100
    tid_show = 101

    t.set_metadata_process(pid_main, 'APP')
    t.set_metadata_thread(pid_main, tid_main, 'MAIN')

    t.snapshot('SNAPSHOT', 
        pid=pid_main, 
        ts=40
    )

    t.counter('COUNTER', 
        pid=pid_main, 
        ts=10, 
        args={'T':5, 'T2': 1}
    )
    t.counter('COUNTER', 
        pid=pid_main, 
        ts=70, 
        args={'T':1, 'T2': 2}
    )

    t.begin('FUNCTION', 
        pid=pid_main, tid=tid_main, 
        ts=0
    )
    t.dur('DUR', 
        pid=pid_main, 
        tid=tid_main, 
        ts=50, dur=100, 
        bind_id='0x1000'
    )
    t.dur('FUNCTION', 
        pid=pid_main, tid=tid_show, 
        ts=70, dur=70
    )
    t.end(pid=pid_main, tid=tid_main, ts=200)
    t.dur('DUR', 
        pid=pid_main, tid=tid_main, 
        ts=250, dur=700, 
        bind_id='0x1000'
    )

    t.begin('FUNCTION', 
        pid=pid_main, tid=tid_show, 
        ts=300)
    t.begin('FUNCTION', 
        pid=pid_main, tid=tid_show, 
        ts=350)
    t.end(pid=pid_main, tid=tid_show, ts=800)

    t.scheduler_running(pid=pid_main, tid=tid_main, ts=100, cpu=1)
    t.scheduler_sleep(pid=pid_main, tid=tid_show, ts=120, cpu=1)


    # t.frame_begin('Frame', pid_main+100, tid_main+100, 400, 0, 'STATE_DROPPED')
    # t.frame_end('Frame', pid_main+100, tid_main+100, 500)


    t.save('test_output')

