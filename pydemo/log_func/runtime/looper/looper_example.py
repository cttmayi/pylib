
def looper(name, args, timestamp, line):
    if name == 'TE':
        if not hasattr(looper, 'last_te_timestamp'):
            looper.last_te_timestamp = timestamp
        else:
            time_diff = (timestamp - looper.last_te_timestamp) / 1000  # 转换为毫秒
            if time_diff > 16:
                print(f"TE interval too long: {time_diff:.2f} ms at line {line}")
            looper.last_te_timestamp = timestamp

def looper_op(name, args, timestamp, line):
    print(f"looper: {name} {args} {timestamp} {line}")
