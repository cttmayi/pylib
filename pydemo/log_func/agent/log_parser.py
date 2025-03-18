from pathlib import Path
from typing import Dict, List, Optional, Union
from qwen_agent.tools.base import register_tool
from lparser.agent.code_helper import PluginAgentHelper


@register_tool('log_parser')
class PluginAgent(PluginAgentHelper):
    description = 'looper函数的python执行环境'
    parameters = [{'name': 'code', 'type': 'string', 'description': '待执行的looper函数代码', 'required': True}]

    RUN_CODE_FILE = str(Path(__file__).absolute().parent / 'resources' / 'log_parser_run_code.py')
    SYSTEM_INSTRUCTION_FILE = str(Path(__file__).absolute().parent / 'resources' / 'log_parser_system_instruction.txt')
    LOG_FILE = str(Path(__file__).absolute().parent / 'resources' / 'data' / 'simple.log')
    COPY_DIRS = ['lparser', 'runtime']

    AGENT_NAME = '日志分析助手'
    AGENT_DESCRIPTION = '我是一个AI日志分析助手。'
    PROMPT_SUGGESTIONS =[{
                            'text': '检查 TE，不应该大于16ms',
                            'files': [LOG_FILE],
                        }]

    def __init__(self, cfg: Optional[Dict] = None):
        cfg = cfg or {}
        cfg['work_dir'] = 'work_dir/workspace'
        super().__init__(cfg)

    def get_run_code(self, code, files):
        with open(PluginAgent.RUN_CODE_FILE, encoding='utf-8') as fin:
            run_code = fin.read()
            run_code = run_code.replace('### <FILES> ###', 'files = ' + str(files))
            run_code = run_code.replace('### <CODE> ###', code)
        return run_code
