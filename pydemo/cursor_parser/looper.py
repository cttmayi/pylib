def looper(name, args, timestamp, line):
    """
    检测 TE 信号，并验证其不应该大于200ms
    同时检查 DQ Buffer 和 Q Buffer 是否配对
    检查 DQ 和 Q Buffer 之间的时间间隔不能超过200ms
    
    Args:
        name: 信号名称
        args: 参数字典
        timestamp: 从log开始的时间戳，单位为微秒
        line: 行号
    """
    # 初始化静态变量
    if not hasattr(looper, "last_te_timestamp"):
        looper.last_te_timestamp = None
    if not hasattr(looper, "buffer_status"):
        looper.buffer_status = {}  # 记录buffer状态，key是buffer id，value是状态('DQ'或'Q')
    if not hasattr(looper, "dq_lines"):
        looper.dq_lines = {}  # 记录DQ操作的行号
    if not hasattr(looper, "dq_timestamps"):
        looper.dq_timestamps = {}  # 记录DQ操作的时间戳
    
    # 检测TE信号
    if name == "panel_te":
        current_timestamp = timestamp
        
        # 如果有上一次TE信号记录
        if looper.last_te_timestamp is not None:
            # 计算时间差（毫秒）
            time_diff = (current_timestamp - looper.last_te_timestamp) / 1000  # 转换为毫秒
            
            # 检测时间间隔是否大于200ms
            if time_diff > 200:
                print(f"警告: TE信号间隔过长 - {time_diff:.2f}ms，超过200ms阈值 (行: {line})")
        
        # 更新最后一次TE信号的时间戳
        looper.last_te_timestamp = current_timestamp
    
    # 检查 DQ Buffer
    elif name == "dq_buffer":
        buffer_id = args.get("id")
        if buffer_id is not None:
            # 检查buffer是否已经被DQ过
            if buffer_id in looper.buffer_status and looper.buffer_status[buffer_id] == 'DQ':
                print(f"警告: Buffer {buffer_id} 被重复DQ (行: {line}，上次DQ行: {looper.dq_lines.get(buffer_id)})")
            
            # 记录buffer状态为DQ
            looper.buffer_status[buffer_id] = 'DQ'
            looper.dq_lines[buffer_id] = line
            looper.dq_timestamps[buffer_id] = timestamp  # 记录DQ的时间戳
    
    # 检查 Q Buffer
    elif name == "q_buffer":
        buffer_id = args.get("id")
        if buffer_id is not None:
            # 检查buffer是否已经被DQ过
            if buffer_id not in looper.buffer_status:
                print(f"警告: Buffer {buffer_id} 在Q之前没有被DQ (行: {line})")
            elif looper.buffer_status[buffer_id] == 'Q':
                print(f"警告: Buffer {buffer_id} 被重复Q (行: {line})")
            else:
                # 检查DQ和Q之间的时间间隔
                dq_timestamp = looper.dq_timestamps.get(buffer_id)
                if dq_timestamp is not None:
                    time_diff = (timestamp - dq_timestamp) / 1000  # 转换为毫秒
                    if time_diff > 200:
                        print(f"警告: Buffer {buffer_id} 的DQ到Q间隔过长 - {time_diff:.2f}ms，超过200ms阈值 (DQ行: {looper.dq_lines.get(buffer_id)}, Q行: {line})")
                
                # 状态正确，DQ后Q，更新状态
                looper.buffer_status[buffer_id] = 'Q' 