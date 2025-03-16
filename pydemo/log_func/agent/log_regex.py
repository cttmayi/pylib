from pathlib import Path
from typing import Dict, List, Optional, Union
from qwen_agent.tools.base import register_tool
from lparser.agent.code_helper import PluginAgentHelper


@register_tool('log_regex')
class PluginAgent(PluginAgentHelper):
    description = 'python执行环境'
    parameters = [{'name': 'code', 'type': 'string', 'description': '待定义的配置代码', 'required': True}]

    RUN_CODE_FILE = str(Path(__file__).absolute().parent / 'resources' / 'log_regex_run_code.py')
    SYSTEM_INSTRUCTION_FILE = str(Path(__file__).absolute().parent / 'resources' / 'log_regex_system_instruction.txt')
    LOG_FILE = str(Path(__file__).absolute().parent / 'resources' / 'data' / 'android.log')
    COPY_DIRS = ['lparser', 'runtime']

    AGENT_NAME = '日志分析助手'
    AGENT_DESCRIPTION = '我是一个AI日志分析助手。'
    PROMPT_SUGGESTIONS =[{
                            'text': '分析上传日志，匹配大于10个',
                            'files': [LOG_FILE],
                        }]

    def __init__(self, cfg: Optional[Dict] = None):
        cfg = cfg or {}
        cfg['work_dir'] = 'work_dir/workspace'
        super().__init__(cfg)

    def get_run_code(self, code, files):
        with open(PluginAgent.RUN_CODE_FILE) as fin:
            run_code = fin.read()
            run_code = run_code.replace('### <FILES> ###', 'files = ' + str(files))
            run_code = run_code.replace('### <CODE> ###', code)
        return run_code