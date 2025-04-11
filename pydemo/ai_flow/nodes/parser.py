from pathlib import Path
from typing import Dict, List, Optional, Union
from pylib.ai.flow import Node, Flow, END
from pylib.ai.flow.nodes import ExecuteRemoteCodeNode, llmNode, ExtractCodeNode
from pylib.ai.flow.const import *
from runtime.op import get_op_infos


RUN_CODE_FILE = str(Path(__file__).absolute().parent / 'resource' / 'run_code.py')
SYSTEM_INSTRUCTION_FILE = str(Path(__file__).absolute().parent / 'resource' / 'system_instruction.txt')

class GenCode(Node):
    COPY_DIRS = ['lparser', 'runtime', 'data']

    def __init__(self):
        super().__init__()


    def execute(self, shared, params):
        code = params
        files = shared[SHARE_FILES] or ['simple.log']
        with open(RUN_CODE_FILE, encoding='utf-8') as fin:
            run_code = fin.read()
            run_code = run_code.replace('### <FILES> ###', 'files = ' + str(files))
            run_code = run_code.replace('### <CODE> ###', code)
        return run_code

class llmGenCode(llmNode):
    def __init__(self):
        with open(SYSTEM_INSTRUCTION_FILE, encoding='utf-8') as fin:
            system_instruction = fin.read()
            system_instruction = system_instruction.replace('### OP_INFOS ###', '\n'.join(get_op_infos()))
        super().__init__(system_prompt=system_instruction, yield_result=True)


class Summary(llmNode):
    def __init__(self):
        system_prompt = '根据用户问题，总结答案'

        super().__init__(system_prompt=system_prompt, yield_result=True)

    def input(self, shared, params):
        user_input = f''' 
用户问题： 
{shared[SHARE_TEXT]}
程序输出：
{params}
        '''
        return user_input
