import lparser.utils.env
from lparser import conf
conf.DEBUG = False
from lparser.main import tool_regex
from lparser.status import Status, OP, ARG

files = None
file = None
### <FILES> ###
file = 'data/log/android.log'

op_map = [
    # 匹配"Failed to find provider info for [provider_name]"格式的日志
    OP('FAILED_PROVIDER', 'Failed to find provider info for %s', info='未能找到指定provider的信息', args=[ARG('provider_name', '提供者名称')]),

    # 匹配"Single process limit 50/s drop [num_lines] lines."格式的日志
    OP('RATE_LIMIT', 'Single process limit 50/s drop %d lines.', info='单进程速率限制导致丢弃日志行', args=[ARG('num_lines', '被丢弃的日志行数')]),

    # 匹配"Unable to instantiate appComponentFactory"及后续堆栈跟踪信息
    OP('APP_COMPONENT_FACTORY', 'Unable to instantiate appComponentFactory\n%s', info='无法实例化appComponentFactory', args=[ARG('stack_trace', '堆栈跟踪信息')]),
    
    # 匹配"ClassLoader.getResources: The class loader returned by Thread.getContextClassLoader() may fail for processes that host multiple applications. You should explicitly specify a context class loader. For example: Thread.setContextClassLoader(getClass().getClassLoader());"
    OP('CLASS_LOADER_WARNING', 'ClassLoader.getResources: The class loader returned by Thread.getContextClassLoader\\(\\) may fail for processes that host multiple applications. You should explicitly specify a context class loader. For example: Thread.setContextClassLoader\\(getClass\\(\\).getClassLoader\\(\\)\\);', info='类加载器警告', args=[]),

    # 匹配关于ClassNotFoundException的堆栈跟踪信息
    OP('CLASS_NOT_FOUND_EXCEPTION', 'java.lang.ClassNotFoundException: Didn\'t find class "%s" on path: DexPathList\[%s\]', info='找不到指定的类', args=[ARG('class_name', '类名'), ARG('path', '路径列表')]),
]

### <CODE> ###



tool_regex(file, op_map=op_map)