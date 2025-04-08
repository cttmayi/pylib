import time
from pylib.ai.flow import Flow, Node, END
from pylib.ai.flow.web import webUI
from pylib.ai.llmv2 import LLM


class llmNode(Node):
    def __init__(self, model="qwen-max"):
        super().__init__()
        self.llm = LLM(model)

    def execute(self, shared, params):
        history = params.get('history', [])
        messages = []
        for message in history:
            if message.get('metadata') is None:
                messages.append(message) 
        messages.append({"role": "user", "content": params['text']})
        # print(messages)
        messages = self.llm.stream(messages)
        for message in messages:
            yield message['content']
        return message['content']


shared_storage = {}
START = Flow()
llm = llmNode()

START >> llm >> END

web = webUI(START)
# web.set_message_transformer(message_to_markdown)
# web.set_message_transformer(message_to_markdown_with_thinking)
web.launch()