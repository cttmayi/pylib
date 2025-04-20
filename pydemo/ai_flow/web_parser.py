

from pylib.ai.flow.web import webUI

from pylib.ai.flow import Flow, END
from pylib.ai.flow.nodes import ExecuteRemoteCodeNode, llmNode, ExtractCodeNode, MCPNode
from pydemo.ai_flow.nodes.parser import GenCode, llmGenCode, Summary




START = Flow()
llm = llmGenCode()
code = ExtractCodeNode()
gen_code = GenCode()
# execute_remote = ExecuteRemoteCodeNode('log_parser')
execute_remote = MCPNode('log_parser', tool_name='execute_code', yield_result=True)
summary = Summary()

START >> llm >> code >> gen_code >> execute_remote >> summary >> END

gui = False
if gui:
    web = webUI(START)
    web.launch()
else:
    iter_ = START.run(params='检测TE')
    for i in iter_:
        print(i)