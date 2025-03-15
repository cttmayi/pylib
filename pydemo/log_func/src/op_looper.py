
# 说明
# 代码会循环调用 op_looper 函数，每次调用都会传入 name, args, timestamp, line 四个参数
# name: 名称
# args: 参数，是一个字典
# timestamp: 时间戳，是一个浮点数，单位是微秒
# line: 行号，是一个整数

# name 类别
# - TE: 表示屏幕TE信号， 无参数
# - FRAME_START: 表示开始绘图， 有一个参数‘id’： 表示buffer id
# - FRAME_END: 表示结束绘图， 有一个参数‘id’： 表示buffer id


def looper(name, args, timestamp, line):
    print(name, args, timestamp, line)
    pass


from main import main
main('log/simple.log', 'debug', looper)