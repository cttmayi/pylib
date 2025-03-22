import re
from functools import lru_cache

FORMAT_PATTERNS = {
    '%b': {'pattern': r'(true|false|True|False|TRUE|FALSE)', 'converter': lambda x: x.lower() == 'true'},
    '%d': {'pattern': r'(-?\d+)', 'converter': int},
    '%s': {'pattern': r'(.*?)', 'converter': str},
    '%f': {'pattern': r'(-?\d+\.\d+)', 'converter': float},
    '%x': {'pattern': r'(0x[0-9A-Fa-f]+|[0-9A-Fa-f]+h|[0-9A-Fa-f]+)', 'converter': lambda x: int(x, 16)},
}

class FormatMatcher:
    def __init__(self, formats, strict_mode = False):
        """
        :param formats: 格式列表，每个元素为 [模式字符串, 变量名列表]
        示例: [["ID: %d, Name: %s", ['id', 'name']], ...]
        """
        self.prefix_map = {}  # 前缀 -> [(format_idx, 正则, 转换器, 变量名列表)]
        self.max_prefix_len = 0
        
        for fmt_idx, (format_str, var_names) in enumerate(formats):
            # 分割格式字符串
            parts = re.split(r'(%\w{1})', format_str)
            placeholders = parts[1::2]  # 提取占位符列表
            
            # 校验占位符数量与变量名数量一致
            if strict_mode and len(placeholders) != len(var_names):
                raise ValueError(f'Format string "{format_str}" has {len(placeholders)} placeholders but {len(var_names)} variable names.')
            
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


if __name__ == '__main__':

    format_number = 100000
    case_number = 100000


    formats = [
        ["ID: %d, Name: %s", ['id', 'name']],
        ["Code: %s-%fs", ['code', 'num'] ],
        ["Score: %d, isTrue: %b", ['score', 'is_true']],
        ["%d-%s-%x" , ['id', 'text', 'letters']],
    ]

    matcher = FormatMatcher(formats)

    # 测试数据
    test_cases = [
        ("ID: 123, Name: Alice", (0, {'id': 123, 'name': 'Alice'})),
        ("Code: XYZ-42.5s", (1, {'code': 'XYZ', 'num': 42.5})),
        ("Score: -5, isTrue: false", (2, {'score': -5, 'is_true': False})),
        ("123-test-0x24", (3, {'id': 123, 'text': 'test', 'letters': 0x24}))
    ] * case_number

    import time
    start_time = time.time()

    for target_str, expected in test_cases:
        result = matcher.match(target_str)
        assert result == expected, f'"{target_str}" failed: {result} != {expected}'

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")


    logs = [
        'printFreezingDisplayLogsopening app wtoken = AppWindowToken{9f4ef63 token=Token{a64f992 ActivityRecord{de9231d u0 com.tencent.qt.qtl/.activity.info.NewsDetailXmlActivity t761}}}, allDrawn= false, startingDisplayed =  false, startingMoved =  false, isRelaunching =  false', 
        'acquire lock=233570404, flags=0x1, tag="View Lock", name=com.android.systemui, ws=null, uid=10037, pid=2227', 
        'ready=true,policy=3,wakefulness=1,wksummary=0x23,uasummary=0x1,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=38,auto=-1,adj=0.0userId=0', 
        'Skipping AppWindowToken{df0798e token=Token{78af589 ActivityRecord{3b04890 u0 com.tencent.qt.qtl/com.tencent.video.player.activity.PlayerActivity t761}}} -- going to hide', 
        'visible is system.time.showampm',
        'shouldBlockLocation  ret:false',
        'mVisiblity.getValue is false',
        'mVisiblity.getValue is false', 'visible is system.charge.show', 'mVisiblity.getValue is false', 'visible is system.call.count gt 0', 'mVisiblity.getValue is false']
    
    regex = [
        ("opening app wtoken = %s, allDrawn= %b, startingDisplayed = %b, startingMoved = %b, isRelaunching = %b", ['wtoken', 'allDrawn', 'startingDisplayed', 'startingMoved', 'isRelaunching']),
        ("acquire lock=%d, flags=%x, tag=\"%s\", name=%s, ws=%s, uid=%d, pid=%d", ['lock', 'flags', 'tag', 'name', 'ws', 'uid', 'pid']),
        ("ready=%b,policy=%d,wakefulness=%d,wksummary=%x,uasummary=%x,bootcompleted=%b,boostinprogress=%b,waitmodeenable=%b,mode=%b,manual=%d,auto=%d,adj=%fuserId=%d", ['ready', 'policy', 'wakefulness', 'wksummary', 'uasummary', 'bootcompleted', 'boostinprogress', 'waitmodeenable', 'mode', 'manual', 'auto', 'adj', 'userId']),
        ("mVisiblity.getValue is %b", ['mVisiblity', 'unknown', 'unknown']),
        ("shouldBlockLocation ret:%b", ['ret']),
    ]

    fm = FormatMatcher(regex)
    for log in logs:
        print(fm.match(log))