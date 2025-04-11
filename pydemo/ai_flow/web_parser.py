

from pylib.ai.flow.web import webUI

from pylib.ai.flow import Node, Flow, END
from pylib.ai.flow.nodes import ExecuteRemoteCodeNode, llmNode, ExtractCodeNode
from pydemo.ai_flow.nodes.parser import GenCode, llmGenCode, Summary




START = Flow()
llm = llmGenCode()
code = ExtractCodeNode()
gen_code = GenCode()
execute_remote = ExecuteRemoteCodeNode()
summary = Summary()

START >> llm >> code >> gen_code >> execute_remote >> summary >> END


web = webUI(START)
web.launch()