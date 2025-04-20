
from pylib.ai.flow.const import *
from pylib.ai.flow import Node
from pylib.ai.llmv2 import LLM
from pylib.ai.utils.mcp_client import ClientSync

class ExtractCodeNode(Node):
    def __init__(self, name=None, yield_result=False):
        super().__init__(name)
        self.yield_result = yield_result

    def execute(self, params):
        from pylib.ai.utils.executor.extract import extract_code_from_markdown
        codes = extract_code_from_markdown(params)
        python_code = None
        python_codes = codes.get('python') or codes.get('inline')
        if python_codes:
            python_code = python_codes[0]
            if self.yield_result:
                yield '\n```python\n' + python_code + '\n```\n'
        return python_code


class ExecuteCodeNode(Node):
    def __init__(self, name=None, yield_result=False):
        super().__init__(name)
        self.yield_result = yield_result

    def execute(self, params):
        from pylib.ai.utils.executor.local import CodeExecutor
        code = params
        executor = CodeExecutor()
        result = executor.call(code)

        if self.yield_result:
            yield result
        return result


class ExecuteRemoteCodeNode(Node):
    def __init__(self, name=None, port: int = 8860, yield_result=False):
        super().__init__(name)
        self.port = port
        self.yield_result = yield_result

    def execute(self, shared, params):
        from pylib.ai.utils.executor.client import send_code_to_server
        request = shared[SHARE_REQUEST]
        host = request.client.host
        code = params
        show = ''
        if self.yield_result:
            show = '正在执行代码...\n```python\n' + code + '\n```\n'
            yield show

        result = send_code_to_server(code, host, self.port)

        stdout = result.get('stdout', '')
        stderr = result.get('stderr', '')
        if stderr:
            yield show + 'Error: ' + stderr
        else:
            yield show + stdout
        return result


class llmNode(Node):
    def __init__(self, model='qwen-max', system_prompt=None, with_history=False, yield_result=False):
        super().__init__()
        self.llm = LLM(model)
        self.system_prompt = system_prompt
        self.need_history = with_history
        self.yield_result = yield_result


    def input(self, shared, params):
        return params

    def execute(self, shared, params):
        params = self.input(shared, params)
        history = shared.get(SHARE_HISTORY, [])
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        if self.need_history:
            for message in history:
                if message.get('metadata') is None: # 移除 thinking 数据
                    messages.append(message)

        content = params.get('text') or params.get('content') if isinstance(params, dict) else params
        messages.append({"role": "user", "content": content})

        messages = self.llm.stream(messages)
        
        for message in messages:
            if self.yield_result:
                yield message['content']

        return message['content']
    

class MCPNode(Node):
    def __init__(self, name=None, host='127.0.0.1', port=8000, tool_name=None, yield_result=False):
        super().__init__(name)
        self.yield_result = yield_result
        self.client = ClientSync(host, port)
        self.tool_name = tool_name

    def execute(self, params):
        code = params

        if self.yield_result:
            show = f'正在执行 {self.tool_name} 工具，请稍候 ...'
            yield show

        result = self.client.call_tool(self.tool_name, code=code)
        if self.yield_result:
            yield result
        return result


if __name__ == '__main__':
    node = MCPNode(tool_name='execute_code', yield_result=True)
    iter_ = node.execute(params='print("Hello, World!")\n') 
    for r in iter_:
        print(r)

    