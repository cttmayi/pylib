def looper(name, args, timestamp, line):
    """
    分析日志中的TE信号间隔，找出间隔大于100ms的情况
    
    参数:
    name: 事件名称
    args: 事件参数字典
    timestamp: 时间戳(微秒)
    line: 行号
    """
    # 只处理TE事件
    if name == 'TE':
        # 初始化静态变量，用于存储上一次TE事件的时间戳
        if not hasattr(looper, 'last_te_timestamp'):
            looper.last_te_timestamp = timestamp
        else:
            # 计算两次TE信号之间的时间间隔(毫秒)
            time_diff = (timestamp - looper.last_te_timestamp) / 1000  # 转换为毫秒
            
            # 检查间隔是否大于100ms
            if time_diff > 100:
                print(f"TE间隔过长: {time_diff:.2f}ms，出现在第{line}行，时间戳: {timestamp}")
            
            # 更新上一次TE事件的时间戳
            looper.last_te_timestamp = timestamp 