import lparser.utils.env
import lparser.conf as conf
from lparser.main import tool_main, tool_main_looper

#获取参数

def config():
    if conf.DEBUG:
        path = 'data/log/simple.log'
        type = None
        path = 'data/android/2k.log'
        type = None

        looper = True
    else:
        import argparse
        parser = argparse.ArgumentParser(description='Parser for log file')
        parser.add_argument('path', type=str, help='log file path')
        parser.add_argument('type', type=str, help='log type')
        parser.add_argument('looper', type=bool, help='loop or not')
        
        args = parser.parse_args()
        path = args.path
        type = args.type
        looper = args.looper
    return path, type, looper

if __name__ == '__main__':
    path, type, looper= config()
    if looper:
        tool_main_looper(path, type)
    else:
        tool_main(path, type)
