import re
import io, sys

from pylib.ai.flow import Node
from pylib.ai.llmv2 import LLM


def extract_code(text: str) -> str:
    code = None
    triple_match = re.search(r'```[^\n]*\n(.+?)```', text, re.DOTALL)
    if triple_match:
        code = triple_match.group(1)

    return code

class ExtractCodeNode(Node):
    def execute(self, params):
        return extract_code(params)

class ExecuteCodeNode(Node):
    def execute(self, params):
        code = params
        result = ''
        if code:
            print('code: ', code)
            output = io.StringIO()
            sys.stdout = output
            try:
                result = eval(code)
            except Exception as e:
                result = str(e)

            sys.stdout = sys.__stdout__
            result = result or output.getvalue().strip()
            output.close()
        yield result
        return result


class llmNode(Node):
    def __init__(self, model, system_prompt=None, need_history=False):
        super().__init__()
        self.llm = LLM(model)
        self.system_prompt = system_prompt
        self.need_history = need_history

    def execute(self, params):
        history = params.get('history', [])
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        if self.need_history:
            for message in history:
                if message.get('metadata') is None: # 移除 thinking 数据
                    messages.append(message)

        content = params.get('text') or params.get('content')
        messages.append({"role": "user", "content": content})

        messages = self.llm.stream(messages)
        for message in messages:
            yield message['content']
        return message['content']