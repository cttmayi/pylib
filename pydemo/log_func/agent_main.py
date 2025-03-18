import lparser.utils.env
import pprint
import os, sys
from pathlib import Path

os.environ['QWEN_AGENT_DEFAULT_WORKSPACE'] = 'work_dir'
# os.environ['QWEN_AGENT_DEBUG'] = '1'

from qwen_agent.gui import WebUI
# from agent.log_regex import PluginAgent
from agent.log_parser import PluginAgent


# 配置您所使用的 LLM。
llm_cfg = {
    # 使用 DashScope 提供的模型服务：
    'model': 'qwen-max',
    'model_server': 'dashscope',
    # 'api_key': 'DASHSCOPE_API_KEY', # 如果这里没有设置 'api_key'，它将读取 `DASHSCOPE_API_KEY` 环境变量。

    # 使用OpenAI,
    # 'model': 'gpt-4o',
    # 'model_server': os.environ['OPENAI_API_BASE'],
    # 'api_key': os.environ['OPENAI_API_KEY'],

    'generate_cfg': {
        'top_p': 0.9
    }
}

is_gui = False

if __name__ == '__main__':
    bot, chatbot_config = PluginAgent.create_agent(llm_cfg)
    if is_gui:
        # GUI
        WebUI(bot, chatbot_config).run()  # bot is the agent defined in the above code, we do not repeat the definition here for saving space.
    else:
        # TUI
        # 执行Plugin 中定义的范例
        query = chatbot_config['prompt.suggestions'][0]['text'] # input('user question: ')
        files = chatbot_config['prompt.suggestions'][0]['files']
        print('user question:', query, files)

        messages = [{
                        'role': 'user', 
                        'content': [{
                            'file': files[0]
                        },{
                            'text': query
                        },]
                    }]
        while True:
            response = []
            for response in bot.run(messages=messages):
                # print('bot response:', response)
                pass
            print('bot response:', response)
            messages.extend(response)

            if True:
                break