import re
from functools import lru_cache

# 预定义格式符的匹配规则和类型转换器
FORMAT_PATTERNS = {
    '%d': {'pattern': r'(-?\d+)', 'converter': int},
    '%s': {'pattern': r'(.+?)', 'converter': str},
    '%l': {'pattern': r'([a-zA-Z]+)', 'converter': str}
}

class FormatMatcher:
    def __init__(self, formats):
        """
        初始化匹配器，预编译所有格式并构建前缀索引
        :param formats: 格式列表，例如 ["ID: %d, Name: %s", ...]
        """
        self.formats = formats
        self.prefix_map = {}  # 前缀 -> [(format_idx, 编译后正则, 转换器列表, 变量列表)]
        self.max_prefix_len = 0
        
        # 预处理所有格式
        for idx, fmt in enumerate(formats):
            # 提取静态前缀和占位符部分
            parts = re.split(r'(%\w+)', fmt)
            static_prefix = parts[0]  # 第一个占位符前的静态部分
            
            # 编译正则
            regex_parts, converters = [], []
            for part in parts:
                if part in FORMAT_PATTERNS:
                    regex_parts.append(FORMAT_PATTERNS[part]['pattern'])
                    converters.append(FORMAT_PATTERNS[part]['converter'])
                elif part and part not in FORMAT_PATTERNS:
                    regex_parts.append(re.escape(part))
            
            # 构建完整正则
            try:
                pattern = re.compile(f'^{"".join(regex_parts)}$')
            except re.error:
                continue  # 跳过无效格式
            
            # 更新前缀索引
            prefix_len = len(static_prefix)
            if prefix_len > 0:
                if static_prefix not in self.prefix_map:
                    self.prefix_map[static_prefix] = []
                self.prefix_map[static_prefix].append(
                    (idx, pattern, converters, parts[1::2]))  # 占位符列表
                self.max_prefix_len = max(self.max_prefix_len, prefix_len)
            else:
                # 处理无静态前缀的格式
                if '' not in self.prefix_map:
                    self.prefix_map[''] = []
                self.prefix_map[''].append(
                    (idx, pattern, converters, parts[1::2]))

    def match(self, target_str):
        """
        匹配字符串，返回匹配到的格式索引和解析结果
        :return: (format_index, parsed_dict) 或 None
        """
        # 优先尝试长前缀匹配
        max_check_len = min(len(target_str), self.max_prefix_len)
        for check_len in range(max_check_len, 0, -1):
            prefix = target_str[:check_len]
            if prefix in self.prefix_map:
                for item in self.prefix_map[prefix]:
                    fmt_idx, pattern, converters, vars_list = item
                    match = pattern.match(target_str)
                    if match:
                        try:
                            parsed = {
                                var: converter(val)
                                for var, val, converter in zip(
                                    vars_list, match.groups(), converters
                                )
                            }
                            return fmt_idx, parsed
                        except ValueError:
                            continue
        # 检查无前缀格式
        if '' in self.prefix_map:
            for item in self.prefix_map['']:
                fmt_idx, pattern, converters, vars_list = item
                match = pattern.match(target_str)
                if match:
                    try:
                        parsed = {
                            var: converter(val)
                            for var, val, converter in zip(
                                vars_list, match.groups(), converters
                            )
                        }
                        return fmt_idx, parsed
                    except ValueError:
                        continue
        return None

formats = [
    "ID: %d, Name: %s",
    "Code: %l-%d",
    "Score: %d",
    # "%d-%s-%l"  # 无静态前缀的格式
] * 1000

formats.append("%d-%s-%l")  # 无静态前缀的格式

matcher = FormatMatcher(formats)

# 测试数据
test_cases = [
    ("ID: 123, Name: Alice", (0, {'%d': 123, '%s': 'Alice'})),
    ("Code: XYZ-42", (1, {'%l': 'XYZ', '%d': 42})),
    ("Score: -5", (2, {'%d': -5})),
    ("123-test-ABC", (3000, {'%d': 123, '%s': 'test', '%l': 'ABC'}))
] * 100000

import time
start_time = time.time()

for target_str, expected in test_cases:
    result = matcher.match(target_str)
    #print(f"Input: {target_str}")
    #print(f"Matched: {result}")
    #print("-" * 40)
    assert result == expected

end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")