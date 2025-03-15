def looper(name, args, timestamp, line):
    print(f"收到{name}信号，参数为{args}，时间戳为{timestamp}，行内容为{line}")
    te_timestamps = {}

    if name == 'TE':
        # 如果这是第一次遇到TE信号或者上一次的TE信号已经被处理过，则初始化或重置时间戳
        if 'last_te' not in te_timestamps:
            te_timestamps['last_te'] = timestamp
        else:
            # 计算与上次TE信号的时间差
            time_diff = timestamp - te_timestamps['last_te']
            
            # 检查时间差是否小于1ms(1000微秒)
            if time_diff < 1000:
                print(f"警告: 在行{line}发现相邻TE信号间隔过短, 仅为{time_diff:.2f}微秒.")
            
            # 更新最后一次TE信号的时间戳
            te_timestamps['last_te'] = timestamp

from lparser.main import tool_main
from lparser.conf import DEBUG
DEBUG = False
tool_main('data/log/simple.log', 'debug', looper)