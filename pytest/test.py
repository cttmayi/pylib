import re

def re_match(format_str, vars_list, target_str):
    # 定义支持的格式符及其正则表达式和类型转换函数
    format_patterns = {
        '%d': {
            'pattern': r'(-?\d+)',          # 匹配整数（含负数）
            'converter': int
        },
        '%s': {
            'pattern': r'(.+?)',            # 非贪婪匹配任意字符（直到下一个静态部分）
            'converter': str
        },
        '%l': {
            'pattern': r'([a-zA-Z]+)',      # 匹配纯字母
            'converter': str
        }
    }
    
    # 分割格式字符串为静态部分和占位符
    parts = re.split(r'(%\w+)', format_str)
    regex_parts = []
    converters = []
    
    for part in parts:
        if part in format_patterns:
            # 处理占位符：添加正则表达式并记录转换函数
            regex_parts.append(format_patterns[part]['pattern'])
            converters.append(format_patterns[part]['converter'])
        elif part:
            # 处理静态部分：转义正则特殊字符
            regex_parts.append(re.escape(part))
    
    # 构建完整正则表达式
    regex_str = ''.join(regex_parts)
    try:
        pattern = re.compile(f'^{regex_str}$', re.DOTALL)
    except re.error:
        return None  # 正则表达式无效
    
    # 执行匹配
    match = pattern.match(target_str)
    if not match:
        return None
    
    # 提取捕获的值并检查数量
    captured_values = match.groups()
    if len(captured_values) != len(vars_list):
        return None
    
    # 转换类型并构建结果字典
    result = {}
    for var, value, converter in zip(vars_list, captured_values, converters):
        try:
            result[var] = converter(value)
        except ValueError:
            return None  # 类型转换失败
    
    return result


# 示例1：基本用法
print(re_match("Name: %s, Age: %d", ["name", "age"], "Name: Alice, Age: 30"))
# 输出: {'name': 'Alice', 'age': 30}

# 示例2：匹配字母（%l）
print(re_match("Code: %l", ["code"], "Code: ABCxy"))
# 输出: {'code': 'ABCxy'}

# 示例3：负数与连续占位符
print(re_match("%d-%s-%l", ["num", "text", "letters"], "-123-hello-World"))
# 输出: {'num': -123, 'text': 'hello', 'letters': 'World'}


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