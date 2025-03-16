import lparser.utils.env
import lparser.conf as conf
from lparser.main import tool_main

#获取参数

def config():
    if conf.DEBUG:
        path = 'data/log/simple.log'
        type = None
    else:
        import argparse
        parser = argparse.ArgumentParser(description='Parser for log file')
        parser.add_argument('path', type=str, help='log file path')
        parser.add_argument('type', type=str, help='log type')
        args = parser.parse_args()
        path = args.path
        type = args.type
    return path, type

if __name__ == '__main__':
    path, type = config()
    tool_main(path, type)
