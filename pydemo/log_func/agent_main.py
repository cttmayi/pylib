import utils.env
import pprint
import os, sys
from qwen_agent.agents import Assistant
from agent.log_parser import CodeInterpreter
from agent.op_info import get_op_info


# 配置您所使用的 LLM。
llm_cfg = {
    # 使用 DashScope 提供的模型服务：
    'model': 'qwen-max',
    'model_server': 'dashscope',
    # 'api_key': 'DASHSCOPE_API_KEY', # 如果这里没有设置 'api_key'，它将读取 `DASHSCOPE_API_KEY` 环境变量。

    # 使用与 OpenAI API 兼容的模型服务，例如 vLLM 或 Ollama：
    # 'model': 'Qwen2-7B-Chat',
    # 'model_server': 'http://localhost:8000/v1',  # base_url，也称为 api_base
    # 'api_key': 'EMPTY',

    'generate_cfg': {
        'top_p': 0.9
    }
}


system_instruction_before = '''你是一个AI助手。
请根据用户请求，参考说明书完善looper函数，并生成代码通过log_parser工具执行。

说明书：
代码会循环调用 op_looper 函数，每次调用都会传入 name, args, timestamp, line 四个参数
- name: 名称
- args: 参数，是一个字典
- timestamp: 时间戳，是一个浮点数，单位是微秒
- line: 行号，是一个整数

# name 类别
'''

system_instruction_after = '''
参考代码如下， 请完善looper函数，并生成代码通过log_parser工具执行。
···python
def looper(name, args, timestamp, line):
    # 请在这里编写代码
    # ···
    pass

from main import main，
main('log/simple.log', 'kernel', looper)。
···
你总是用中文回复用户。'''

# 创建一个智能体。这里我们以 `Assistant` 智能体为例，它能够使用工具并读取文件。
system_instruction = []
system_instruction.append(system_instruction_before)
system_instruction.extend(get_op_info('debug'))
system_instruction.append(system_instruction_after)
system_instruction = '\n'.join(system_instruction)
print(system_instruction)


tools = [
    {'name': 'log_parser', 'work_dir': '~/temp/workspace',},
    ]
files = ['./op_looper.py']
bot = Assistant(llm=llm_cfg,
                system_message=system_instruction,
                function_list=tools,
                files=files,
                )

# 作为聊天机器人运行智能体。
from qwen_agent.gui import WebUI
WebUI(bot).run()  # bot is the agent defined in the above code, we do not repeat the definition here for saving space.
