





def func(state):
    if state.time('am_proc', 'start', 'died') > 5000:
        return f"进程数量异常"
    return None