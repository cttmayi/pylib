import re
import io, sys

from pylib.ai.flow import Node
from pylib.ai.llmv2 import LLM


def extract_code_from_markdown(markdown_text):
    """
    从Markdown文本中提取代码块和行内代码。
    参数:
        markdown_text (str): Markdown格式的文本。
    返回:
        dict: 包含代码块和行内代码的列表。
    """
    # 匹配代码块（包括语言标识和代码内容）
    block_pattern = r"```(\w+)?\n([\s\S]+?)\n```"
    # 匹配行内代码
    inline_pattern = r"`([^`\n]+)`"

    result = {}
    # 先匹配代码块
    for match in re.finditer(block_pattern, markdown_text):
        language = match.group(1) if match.group(1) else "plaintext"
        code = match.group(2).strip()
        if language not in result:
            result[language] = []
        result[language].append(code)

    # 再匹配行内代码
    for match in re.finditer(inline_pattern, markdown_text):
        if language not in result:
            result[language] = []
        result[language].append(code)

    return result

def is_python_code(code_str):
    try:
        compile(code_str, '<string>', 'exec')
        return True
    except SyntaxError:
        return False

class ExtractCodeNode(Node):
    def execute(self, params):
        codes = extract_code_from_markdown(params)
        python_code = codes.get('python') or codes.get('inline') 
        if python_code:
            return python_code[0]
        if is_python_code(params):
            return params
        return None


def replace_print_with_assignment(code):
    code = code.strip()
    if code.startswith('print(') and code.endswith(')'):
        new_code = code[6:-1]
        return new_code
    else:
        return code  # 如果不符合格式，返回原字符串


class ExecuteCodeNode(Node):
    def execute(self, params):
        from pylib.ai.utils.executor import CodeExecutor
        code = params
        executor = CodeExecutor()
        result = executor.call(code)

        yield result
        return result


class llmNode(Node):
    def __init__(self, model, system_prompt=None, with_history=False):
        super().__init__()
        self.llm = LLM(model)
        self.system_prompt = system_prompt
        self.need_history = with_history

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
    

if __name__ == '__main__':
    code = """
from sympy import symbols, Eq, solve
x = symbols('x')
equation = Eq(x + 1, 2*x)
solution = solve(equation, x)

solution[0]

def calculate_24(nums):
    return 0

print(calculate_24(0))
"""
    if is_python_code(code):
        print(run_python_code(code))

    