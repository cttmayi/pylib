

from trace_processor.api import TraceProcessor # pip install trace_processor

import os

path = 'test_data/android/trace/trace.pftrace'

if os.path.isfile(path):
    tp = TraceProcessor(file_path=path)

    qr_it = tp.query('SELECT ts, dur, name FROM slice')
    for row in qr_it:
        print(row.ts, row.dur, row.name)