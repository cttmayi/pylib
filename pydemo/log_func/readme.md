
conf.py 配置文件
    DEBUG: 是否开启debug模式

parser.__init__.py 日志解析器配置
添加不同类型的日志解析器

PARSER_MAP = {
    'debug': debug_parser,
    'main':  main_parser,
}