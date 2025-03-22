import pylib.env
from pprint import pprint
from pylib.basic.re_exp.re_exp2 import FormatMatcher
from pylib.ai.llm import LLM
from pylib.basic.file import log_read


llm = LLM("qwen-plus", systmem_prompt='你是代码生成专家，请根据用户需求生成表达式')

REGEX_NAME = 'regex'

def code_gen(log_msg_list, office, max_row=3):
    log_msg = '\n'.join(log_msg_list[office:office+max_row])
    prompt = f'''请根据以下日志信息生成代码，请使用%d、%s、%b、%f、%x等格式化符号，并根据日志猜测参数名（如无法猜测， 使用unknown），请严格按照空格个数匹配，不要使用正则表达式的转义字符
请直接生成代码，不要输出任何解释
例如，

日志信息：
manufacture: MK isGUI: false, true
生成代码：
···python
{REGEX_NAME} = [
    ("manufacture: %s isGUI: %b, %b“, ['manufacture', 'isGUI', 'unknown']),
    ]
···

日志信息：
'''
    prompt += log_msg
    prompt += r'''请直接生成代码
'''
    message = llm.chat(prompt)
    codes = llm.content_filter(message)
    return codes[0]['content'] if len(codes) > 0 and codes[0]['type'] == 'python' else None

def code_gen_retry():
    prompt = '你提供的代码完全没有匹配成功，请重新生成提供'
    message = llm.chat(prompt)
    codes = llm.content_filter(message)
    return codes[0]['content'] if len(codes) > 0 and codes[0]['type'] == 'python' else None


def code_exec(code, arg_name):    
    namespace = {}
    if code is not None:
        exec(code, namespace)
    regex = namespace.get('regex', None)
    return regex


def filter_log_msg_list(log_msg_list, regex_list):
    if len(regex_list) > 0:
        fm = FormatMatcher(regex_list)
        new_log_msg_list = []
        for log in log_msg_list:
            match = fm.match(log)
            if match is None:
                new_log_msg_list.append(log)
    else:
        new_log_msg_list = log_msg_list

    return new_log_msg_list


def regex_verify(regex, log_msg_list):
    regex_list = []
    if regex:
        fm = FormatMatcher(regex)
        for log in log_msg_list:
            match = fm.match(log)
            if match is not None:
                regex_pattern:str = regex[match[0]][0]
                regex_args = regex[match[0]][1]

                if regex_pattern not in [x[0] for x in regex_list]: #检查是否pattern 是否重复
                    if regex_pattern.count('%') <= len(regex_args):
                        regex_args = regex_args[:regex_pattern.count('%')]

                    regex_list.append((regex_pattern, regex_args))

    return regex_list

if __name__ == '__main__':
    log_list, _ = log_read('data/2k.log')

    log_msg_list = []
    for log in log_list:
        log_msg_list.append(log['msg'])

    log_msg_list = log_msg_list[:100]
    # print('--- log_msg_list ---')
    # print(log_msg_list)

    regex_list = []
    looper = 0
    retry = 0
    offset = 0
    while(looper < 30 and len(log_msg_list) > offset):
        looper += 1

        log_msg_list = filter_log_msg_list(log_msg_list, regex_list)
        if retry > 0:
            code = code_gen_retry()
        else:
            code = code_gen(log_msg_list, offset, 5)

        print('--- code ---')
        print(code)

        regex = code_exec(code, REGEX_NAME)
        extend_regex = regex_verify(regex, log_msg_list)

        if len(extend_regex) > 0:
            llm.reset()
            regex_list.extend(extend_regex)
            retry = 0
        else:
            retry += 1
            if retry == 3:
                llm.reset()
                retry = 0
                offset += 5
        
        print(f'\r{looper:03d}: 剩余日志数: {len(log_msg_list)}, 生成的regex数量: {len(regex_list)}', end='')

    print()
    print('--- final result ---')
    print(f'剩余日志数：{len(log_msg_list)}')
    for id, regex in enumerate(log_msg_list):
        print(f'log[{id}]: {regex}')
    print(f'生成的regex数量：{len(regex_list)}')
    print('regex_list = [')
    for id, regex in enumerate(regex_list):
        print(f'    {regex},')
    print(']')




