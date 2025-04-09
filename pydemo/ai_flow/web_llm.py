import time
from pylib.ai.flow import Flow, Node, END
from pylib.ai.flow.web import webUI
from pylib.ai.flow.nodes import ExtractCodeNode, ExecuteCodeNode, llmNode

shared_storage = {}
START = Flow()
llm = llmNode(model='qwen-max', system_prompt='请你根据客户提问，用python代码回答，最后print打印出结果', with_history=True)
coder = ExtractCodeNode()
executor = ExecuteCodeNode()

START >> llm >> coder >> executor >> END

web = webUI(START)
# web.set_message_transformer(message_to_markdown)
# web.set_message_transformer(message_to_markdown_with_thinking)
web.launch()