import re
from functools import lru_cache

FORMAT_PATTERNS = {
    '%d': {'pattern': r'(-?\d+)', 'converter': int},
    '%s': {'pattern': r'(.+?)', 'converter': str},
    '%l': {'pattern': r'([a-zA-Z]+)', 'converter': str}
}

class FormatMatcher:
    def __init__(self, formats):
        """
        :param formats: 格式列表，每个元素为 [模式字符串, 变量名列表]
        示例: [["ID: %d, Name: %s", ['id', 'name']], ...]
        """
        self.prefix_map = {}  # 前缀 -> [(format_idx, 正则, 转换器, 变量名列表)]
        self.max_prefix_len = 0
        
        for fmt_idx, (format_str, var_names) in enumerate(formats):
            # 分割格式字符串
            parts = re.split(r'(%\w+)', format_str)
            placeholders = parts[1::2]  # 提取占位符列表
            
            # 校验占位符数量与变量名数量一致
            if len(placeholders) != len(var_names):
                continue  # 跳过无效格式
            
            # 构建正则表达式
            regex_parts, converters = [], []
            for part in parts:
                if part in FORMAT_PATTERNS:
                    regex_parts.append(FORMAT_PATTERNS[part]['pattern'])
                    converters.append(FORMAT_PATTERNS[part]['converter'])
                elif part:
                    regex_parts.append(re.escape(part))
            
            try:
                pattern = re.compile(f'^{"".join(regex_parts)}$')
            except re.error:
                continue
            
            # 提取静态前缀
            static_prefix = parts[0]
            prefix_len = len(static_prefix)
            
            # 更新前缀索引
            if prefix_len > 0:
                if static_prefix not in self.prefix_map:
                    self.prefix_map[static_prefix] = []
                self.prefix_map[static_prefix].append(
                    (fmt_idx, pattern, converters, var_names)
                )
                self.max_prefix_len = max(self.max_prefix_len, prefix_len)
            else:
                if '' not in self.prefix_map:
                    self.prefix_map[''] = []
                self.prefix_map[''].append(
                    (fmt_idx, pattern, converters, var_names)
                )

    def match(self, target_str):
        """返回匹配结果 (格式索引, 解析字典) 或 None"""
        max_check_len = min(len(target_str), self.max_prefix_len)
        for check_len in range(max_check_len, 0, -1):
            prefix = target_str[:check_len]
            if prefix in self.prefix_map:
                for item in self.prefix_map[prefix]:
                    fmt_idx, pattern, converters, var_names = item
                    match = pattern.match(target_str)
                    if match:
                        try:
                            parsed = {
                                var: converter(val)
                                for var, val, converter in zip(
                                    var_names, match.groups(), converters
                                )
                            }
                            return fmt_idx, parsed
                        except ValueError:
                            continue
        # 处理无前缀格式
        if '' in self.prefix_map:
            for item in self.prefix_map['']:
                fmt_idx, pattern, converters, var_names = item
                match = pattern.match(target_str)
                if match:
                    try:
                        parsed = {
                            var: converter(val)
                            for var, val, converter in zip(
                                var_names, match.groups(), converters
                            )
                        }
                        return fmt_idx, parsed
                    except ValueError:
                        continue
        return None
    
formats = [
    ["ID: %d, Name: %s", ['id', 'name']],
    ["Code: %l-%d", ['code', 'num'] ],
    ["Score: %d", ['score']],
    ["%d-%s-%l" , ['id', 'text', 'letters']],
]

matcher = FormatMatcher(formats)

# 测试匹配
test_cases = [
    "ID: 123, Name: Alice",
    "Code: XYZ-42",
    "Score: -5",
    "123-hello-World"
]

for s in test_cases:
    result = matcher.match(s)
    if result:
        fmt_idx, parsed = result
        print(f"匹配到格式[{fmt_idx}]: {parsed}")
    else:
        print(f"未匹配: {s}")