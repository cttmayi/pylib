import time
import gradio as gr
from pylib.ai.flow import Flow

class webUI:
    def __init__(self, start:Flow):
        self.start = start
        self.message_transformer = message_to_chatmessage

    def set_message_transformer(self, message_transformer):
        self.message_transformer = message_transformer

    def echo(self, message, history):
        response = []

        if not isinstance(message, dict):
            message = {'text': message}

        message['history'] = history

        files = message.get('files')
        for file in files:
            response.append(gr.File(value=file))

        shared_storage = {}
        iter_= self.start.run(shared_storage, params=message)
        for msg in self.message_transformer(iter_):
            if not isinstance(msg, list):
                msg = [msg]
            yield response + msg

    def launch(self):
        with gr.Blocks(fill_height=True) as demo:
            gr.ChatInterface(
                fn=self.echo, 
                type="messages",
                multimodal=True,
                textbox=gr.MultimodalTextbox(file_count="multiple"),
            )
        demo.launch()


def message_to_markdown(messages_iter):
    for messages in messages_iter:
        message = messages[-1]
        if message['role'] == 'End':
            content = message['content']
            yield content

def message_to_markdown_with_thinking(messages_iter):
    for messages in messages_iter:
        content = "## 思考\n"
        for message in messages:
            if message['content'] is not None:
                content += f"{message['role']}: {message['content']}\n"
        yield content
    content += "## 答案\n"
    content += f"{message['content']}\n"
    yield content

def message_to_chatmessage(messages_iter):
    from gradio import ChatMessage
    start_time = time.time()
    response = ChatMessage(
        role="assistant",
        content="",
        metadata={"title": "正进行推理 ...", "id": 0, "status": "pending"}
    )
    yield response

    for messages in messages_iter:
        content = ''
        for message in messages:
            thought_role = message['role']
            thought_content = message['content']
            if thought_content is not None:
                content += f"- {thought_role}: {thought_content}\n"
        response.content = content
        yield response

    response.metadata["status"] = "done"
    response.metadata["duration"] = time.time() - start_time
    response.metadata["title"] = "已完成推理"
    yield response

    response = [
        response,
        ChatMessage(
            role="assistant",
            content= message['content']
        )
    ]
    yield response



if __name__ == '__main__':
    from pylib.ai.flow import Flow, Node, END

    class WebTransformerNode(Node):
        def execute(self, shared, params):
            text = params['text']
            try :
                number = int(text)
            except:
                number = len(text)
            return number

    class NumberNode(Node):
        def __init__(self, number):
            super().__init__(verbose=True)
            self.number = number

        def execute(self, shared, params):
            shared['current'] = params or self.number
            return shared['current']

    class AddNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def execute(self, shared, params):
            current = shared['current']
            v = 1 if self.number >= 0 else -1
            for _ in range(abs(self.number)):
                current += v
                yield current
                time.sleep(0.1)
            
            shared['current'] = current
            return shared['current']

    class MultiplyNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def execute(self, shared, params):
            shared['current'] *= self.number
            return shared['current']

    class CheckPositiveNode(Node):
        def if_cond(self, shared, params):
            if shared['current'] >= 0:
                return 'positive'
            else:
                return 'negative'

    shared_storage = {}
    START = Flow()
    web = WebTransformerNode()
    n1 = NumberNode(10)
    check = CheckPositiveNode()
    subtract3 = AddNode(-3)

    START >> web >> n1 >> check('positive') >> subtract3 >> check('negative')  >> END

    web = webUI(START)
    # web.set_message_transformer(message_to_markdown)
    # web.set_message_transformer(message_to_markdown_with_thinking)
    web.launch()