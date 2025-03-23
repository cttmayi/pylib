import pylib.env
import os
from pprint import pprint
from pylib.basic.re_exp.re_exp2 import FormatMatcher
from pylib.ai.llm import LLM
from pylib.basic.file import log_read, jsonl_write, jsonl_read
from pylib.basic.print import print_blue

from pylib.ai.agent import Agent, Router

USER = 'User'
CODE_GENERATOR = 'Code Generator'
CODE_VALIDATOR = 'Code Validator'

REGEX_NAME = 'regex'

PROMPT_VERIFY_SUCCESS = '验证成功'
PROMPT_VERIFY_FAIL = '验证失败， 完全不能匹配，请重新编码'
PROMPT_CODING_FAIL = '执行失败，编码错误，请重新编码，如无一直错误，可以减少匹配数量'
PROMPT_PATTERN_TOO_SIMPLE = '编写的Pattern太简单，会导致很容易匹配全部，请重新编码'
PROMPT_VERIFY_RETRY = '无法匹配，请重新编码'


def code_exec(code):    
    namespace = {}
    if code is not None:
        exec(code, namespace)
    regex = namespace.get(REGEX_NAME, None)
    return regex

def regex_verify(regex, log_msg_list):
    regex_list = []
    if regex:
        try:
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
        except Exception as e:
            print(e)
            regex_list = None
            pass
    return regex_list


class CodeGenerator(Agent):
    def __init__(self):
        self.llm = LLM("qwen-plus", systmem_prompt='你是代码生成专家，请根据用户需求生成表达式')
        self.data = None

    def chat(self, prompt, data, new_task, **kwargs):
        if new_task:
            self.llm.reset()
            self.data = data
        return self.message_reply(CODE_VALIDATOR, self.llm.chat(prompt), self.data)


class User(Agent):
    def __init__(self, log_path, max_row=None, template_path=None):
        log_list, _ = log_read(log_path)

        self.log_msg_list = []
        for log in log_list:
            self.log_msg_list.append(log['msg'])

        if max_row is not None:
            self.log_msg_list = self.log_msg_list[:max_row]

        self.log_msg_offset = 0
        self.template_path = template_path
        self.regex_list = self.load_template_file()
        self.log_msg_list = self.filter_log_msg_list()
        pass

    def new_task_prompt(self, log_msg_list):
        log_msg = '\n'.join(log_msg_list)
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
        prompt += f'''
请直接生成代码, 注意， 有大量需要匹配的日志， 尽量写得通用。
'''
        return prompt

    def filter_log_msg_list(self):
        if len(self.regex_list) > 0:
            fm = FormatMatcher(self.regex_list)
            new_log_msg_list = []
            for log in self.log_msg_list:
                match = fm.match(log)
                if match is None:
                    new_log_msg_list.append(log)
        else:
            new_log_msg_list = self.log_msg_list

        return new_log_msg_list

    def status(self, final=True):
        if final:
            print_blue('--- Final Result ---')
        else:
            print_blue('--- Current Result ---')
        print(f'剩余日志数：{len(self.log_msg_list)}')
        if final:
            for id, regex in enumerate(self.log_msg_list):
                print(f'log[{id}]: {regex}')
        print(f'生成的regex数量：{len(self.regex_list)}')


    def load_template_file(self):
        regex_list = []
        if self.template_path is not None and os.path.exists(self.template_path):
            template_map = jsonl_read(self.template_path)
            for template in template_map:
                regex_list.append((template['EventTemplate'], template['EventArgs']))
        return regex_list

    def save_template_file(self):
        if self.template_path is not None:
            regex_map = [{'EventId': f'E{e:04d}', 'EventTemplate': regex[0], 'EventArgs': regex[1]} for e, regex in enumerate(self.regex_list)]
            jsonl_write(self.template_path, regex_map)


    def chat(self, prompt:str, data, from_role, **kwargs):
        size = 500
        # print(prompt, data, from_role)
        if prompt.startswith(PROMPT_VERIFY_SUCCESS) and from_role == CODE_VALIDATOR:
            self.regex_list.extend(data)
            self.log_msg_list = self.filter_log_msg_list()
            self.status(final=False)
            self.save_template_file()
        elif prompt == PROMPT_VERIFY_FAIL:
            self.log_msg_offset += size

        if len(self.log_msg_list) <= self.log_msg_offset:
            self.save_template_file()
            return self.message_end()
        else:
            current_log_msg = self.log_msg_list[self.log_msg_offset: self.log_msg_offset+size]
            prompt = self.new_task_prompt(current_log_msg)
            return self.message_new_task(CODE_GENERATOR, prompt, current_log_msg)


class CodeVilidator(Agent):
    def __init__(self, max_retry=3):
        self.retry = 0
        self.max_retry = max_retry

    def chat(self, prompt, data, **kwargs):
        codes = LLM.content_filter(prompt)
        code = codes[0]['content'] if len(codes) > 0 and codes[0]['type'] == 'python' else None
        if code is not None:
            regex_list = code_exec(code)
            extend_regex = regex_verify(regex_list, data)

            for regex in regex_list:
                pattern = regex[0]
                if pattern in [r'%s', ] :
                    if self.retry < self.max_retry:
                        self.retry += 1
                        return self.message_reply(CODE_GENERATOR, PROMPT_PATTERN_TOO_SIMPLE + '\n错误的编码范例：pattern=' + pattern )
                    self.retry = 0
                    return self.message_reply(USER, PROMPT_VERIFY_FAIL)
            if extend_regex is None:
                return self.message_reply(USER, PROMPT_CODING_FAIL)
            elif len(extend_regex) > 0:
                self.retry = 0
                return self.message_reply(USER, PROMPT_VERIFY_SUCCESS + ' (' + str(len(extend_regex)) + '/' + str(len(regex_list)) + ')', extend_regex)
            else:
                if self.retry < self.max_retry:
                    self.retry += 1
                    return self.message_reply(CODE_GENERATOR, PROMPT_VERIFY_RETRY)
                self.retry = 0
                return self.message_reply(USER, PROMPT_VERIFY_FAIL)     
        else:
            return self.message_reply(USER, PROMPT_CODING_FAIL)
                

if __name__ == '__main__':
    log_path = 'data/android/2k.log'
    log_size = None
    template_path = 'data/android/templates.jsonl'

    router = Router(verbose=True)
    user = User(log_path, log_size, template_path=template_path)
    router.add_agent(USER, user)
    router.add_agent(CODE_GENERATOR, CodeGenerator())
    router.add_agent(CODE_VALIDATOR, CodeVilidator())
    router.run()

    user.status()
    user.save_template_file()



        




