


def func(state):
    # v = state.get('freq')

    if state.time('freq', 'TE') < 50000:
        return f"创建频繁"
    return None