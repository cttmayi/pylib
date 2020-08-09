import re

# 简化正则表达式, 用类似printf的方式去匹配

_values = {
    'x': r'([\da-fA-F]{1,})', # 16进制的数字, 不包括前面的0x, 比如 F9, 55
    'd': r'([+-]{0,1}\d{1,})', # 10进制的数字
    's': r'([\da-zA-Z\.]{1,}[\da-zA-Z]{1,})', # 字符串
    'a': r'(.+)',
    'X': r'[\da-fA-F]{1,}',
    'D': r'[+-]{0,1}\d{1,}',
    'S': r'[\da-zA-Z\.]{1,}[\da-zA-Z]{1,}',
    'a': r'.+',
}


def re_exp(cond):
    cond_arr = []
    is_replace = False
    for i in range(len(cond)):
        c = cond[i]
        if c == '%':
            is_replace = True
        elif is_replace:
            if c in _values.keys():
                cond_arr.append(_values[c])
            elif c in ['0', '1']:
                cond_arr.append('%')
                cond_arr.append(c)
            is_replace = False
        elif c in [ '(', ')', '\\', '[', ']', '-', '.']:
            cond_arr.append('\\')
            cond_arr.append(c)
        else:
            cond_arr.append(c)    
    
    cond =  ''.join(cond_arr)
    return cond


if __name__ == '__main__': # 测试
    pat = re_exp(r'[%d,%d,%d,%s,%s,%s/%s]')

    r = re.compile(pat) 
    m = r.match(r'[0,1552,1000,com.mediatek.atci.service,broadcast,com.mediatek.atci.service/.AtciIntentReceiver]')
    result = m.groups()

    print(result)

    answer = ('0', '1552', '1000', 'com.mediatek.atci.service', 'broadcast', 'com.mediatek.atci.service', '.AtciIntentReceiver')

    for i, a in enumerate(answer):
        r = result[i]
        if r == a:
            print('PASS')
        else:
            print('FAIL', r, a)
    




