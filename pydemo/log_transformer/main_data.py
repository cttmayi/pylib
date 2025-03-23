import pylib.env
from pylib.basic.re_exp.re_exp2 import FormatMatcher
from pylib.basic.file import log_read, jsonl_read, jsonl_write





def load_template(template_path):
    templates = []
    template_rows = jsonl_read(template_path)
    template_rows.sort(key=lambda x: len(x['EventTemplate']), reverse=True) # sort by length of template
    for row in template_rows:
        event_template = row['EventTemplate']
        event_args = row['EventArgs']
        templates.append((event_template, event_args))
    fm = FormatMatcher(templates)
    return fm, template_rows

def transfer_log_data(fm, log_path, log_structured_path, template_rows):
    log_rows, _ = log_read(log_path)
    print('Log file:', log_path)
    print('Total lines: ', len(log_rows))
    # LineId,Date,Time,Pid,Tid,Level,Component,Content,EventId,EventTemplate,EventArgs
    logs = []
    error_line_num = 0
    for line_id, row in enumerate(log_rows):
        event_id, args = fm.match(row['msg'])
        if event_id is not None:
            log = {}
            log['LineId'] = line_id + 1
            log['Date'] = row['date']
            log['Time'] = row['time']
            log['Pid'] = row['pid']
            log['Tid'] = row['tid']
            log['Level'] = row['level']
            log['Component'] = row['tag']
            log['Content'] = row['msg']
            log['EventId'] = template_rows[event_id]['EventId']
            log['EventTemplate'] = template_rows[event_id]['EventTemplate']
            log['EventArgs'] = args
            logs.append(log)
        else:
            error_line_num += 1

    print('No Matched lines: ', error_line_num)
    print('Matched lines: ', len(logs))

    jsonl_write(log_structured_path, logs)


if __name__ == '__main__':
    log_path = 'data/android/2k.log'
    template_path = 'data/android/templates.jsonl'
    log_structured_path = log_path + '_structured.jsonl'

    fm, template_rows = load_template(template_path)
    transfer_log_data(fm, 'data/android/2k.log', 'data/android/2k.jsonl', template_rows)
    transfer_log_data(fm, 'data/android/1M.log', 'data/android/1M.jsonl', template_rows)
    print('Done!')