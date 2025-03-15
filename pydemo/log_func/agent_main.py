import utils.env
import pprint
import shutil
import os, sys
from pathlib import Path
os.environ['QWEN_AGENT_DEFAULT_WORKSPACE'] = 'work_dir'
from qwen_agent.agents import Assistant
from lparser.agent.log_parser import CodeInterpreter, SYSTEM_INSTRUCTION_FILE, USER_PICTURE_FILE, AGENT_PICTURE_FILE
from lparser.agent.op_info import get_op_info

PARSER_WORKSPACE = 'work_dir/workspace'

def copy_dir(src_dir):
    dst_dir = os.path.join(PARSER_WORKSPACE, src_dir)
    shutil.copytree(src_dir, dst_dir,symlinks=True, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'), dirs_exist_ok=True)

os.makedirs(PARSER_WORKSPACE, exist_ok=True)
copy_dir('lparser')
copy_dir('runtime')
copy_dir('data')


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

# 创建一个智能体。这里我们以 `Assistant` 智能体为例，它能够使用工具并读取文件。
with open(SYSTEM_INSTRUCTION_FILE, 'r') as f:
    system_instruction = f.read()
    system_instruction = system_instruction.replace('<OP_LIST>', '\n'.join(get_op_info('debug')))


tools = [
    {'name': 'log_parser', 'work_dir': PARSER_WORKSPACE,},
    ]
# files = ['./op_looper.py']
bot = Assistant(llm=llm_cfg,
                system_message=system_instruction,
                function_list=tools,
                # files=files,
                description='我是一个日志分析助手',
                )


chatbot_config = {
    'input.placeholder': '请输入需要检查的内容',
    'prompt.suggestions': ['检查 TE，不应该大于16ms'],
    'user.avatar': USER_PICTURE_FILE,
    'agent.avatar': AGENT_PICTURE_FILE,
}

# 作为聊天机器人运行智能体。
from qwen_agent.gui import WebUI
WebUI(bot, chatbot_config).run()  # bot is the agent defined in the above code, we do not repeat the definition here for saving space.
