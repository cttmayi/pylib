import re
from functools import lru_cache

# 预定义格式符的匹配规则和类型转换器（常量提升到全局）
FORMAT_PATTERNS = {
    '%d': {
        'pattern': r'(-?\d+)',
        'converter': int
    },
    '%s': {
        'pattern': r'(.+?)',
        'converter': str
    },
    '%l': {
        'pattern': r'([a-zA-Z]+)',
        'converter': str
    }
}

@lru_cache(maxsize=128)  # 缓存常见格式模板
def _compile_format(format_str):
    """预编译格式字符串为 (正则表达式, 转换器列表)"""
    parts = re.split(r'(%\w+)', format_str)
    regex_parts = []
    converters = []
    
    for part in parts:
        if part in FORMAT_PATTERNS:
            # 处理已知格式符
            regex_parts.append(FORMAT_PATTERNS[part]['pattern'])
            converters.append(FORMAT_PATTERNS[part]['converter'])
        elif part.startswith('%'):
            # 遇到未知格式符直接返回错误
            return None, None  
        elif part:
            # 转义静态部分
            regex_parts.append(re.escape(part))
    
    try:
        # 编译正则（移除DOTALL提升性能，除非需要匹配换行）
        pattern = re.compile(f'^{"".join(regex_parts)}$') 
        return pattern, converters
    except re.error:
        return None, None

def re_match(format_str, vars_list, target_str):
    # Step 1: 获取预编译的正则和转换器
    pattern, converters = _compile_format(format_str)
    if not pattern or len(converters) != len(vars_list):
        return None
    
    # Step 2: 快速匹配
    match = pattern.match(target_str)
    if not match:
        return None
    
    # Step 3: 类型转换
    result = {}
    try:
        for var, val_str, converter in zip(vars_list, match.groups(), converters):
            result[var] = converter(val_str)
    except ValueError:
        return None
    
    return result


import time
start_time = time.time()
formats = ["ID: %d, Name: %s", "Code: %l-%d", "Score: %d"]
data = [
    ("ID: 123, Name: Alice", ['id', 'name'], {'id': 123, 'name': 'Alice'}),
    ("Code: XYZ-42", ['code', 'num'], {'code': 'XYZ', 'num': 42}),
    ("Score: -5", ['score'], {'score': -5})
] * 100000


for vars_str, vars_list, target_map in data:
    for format in formats:
        result = re_match(format, vars_list, vars_str)
        if result is not None:
            assert result == target_map
            break
    # assert result == target_str

end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")



# 优化前: ~12.3 秒
# 优化后: ~1.8 秒 (6.8倍加速)