import time
import gradio as gr
from pylib.ai.flow import Flow

class webUI:
    def __init__(self, start:Flow, **kwargs):
        self.start = start
        # self.title = kwargs.get("title", "AI Robot"),
        # self.description = kwargs.get("description", "Ask AI Robot any question"),
        # self.theme = kwargs.get('theme', "ocean"),
        # self.examples = # ["Hello", "Am I cool?", "Are tomatoes vegetables?"],
        self.message_transformer = message_to_chatmessage

    def set_message_transformer(self, message_transformer):
        self.message_transformer = message_transformer

    def response(self, message, history, state):
        responses = []
        if not isinstance(message, dict):
            message = {'text': message}
        message['history'] = history

        message_iter = state.get('message_iter', None)
        if message_iter is not None:
            try:
                shared_storage = state.get('shared_storage', {})
                message_iter.send(message['text'])
            except StopIteration:
                shared_storage = {}
                message_iter = self.start.run(shared_storage, params=message)
        else:
            shared_storage = {}
            message_iter = self.start.run(shared_storage, params=message)


        state['message_iter'] = message_iter
        state['shared_storage'] = shared_storage

        response_iter = self.message_transformer(message_iter)

        while True:
            try:
                response = next(response_iter)
                if not isinstance(response, list):
                    response = [response]
                yield responses + response
            except StopIteration:
                break

    def launch(self):
        with gr.Blocks(fill_height=True) as demo:
            gr.ChatInterface(
                fn=self.response, 
                type="messages",
                multimodal=True,
                textbox=gr.MultimodalTextbox(file_count="multiple"),
                # title=self.title,
                # description=self.description,
                # theme=self.theme,
                additional_inputs=[
                    gr.State({}),
                ],
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
    response_thinking = ChatMessage(
        role="assistant",
        content="",
        metadata={"title": "正进行推理 ...", "id": 0, "status": "pending"},
    )
    response_answer = ChatMessage(
        role="assistant",
        content= '',
    )

    for messages in messages_iter:
        response_thinking.content = ''
        response_answer.content = ''
        for message in messages:
            thought_role = message['role']
            thought_content = message['content']
            thought_interrupt = message['interrupt']
            is_thought = not message['answer']
            is_input_message = message['category'] == 'start'

            if is_input_message:
                continue

            if thought_content is not None:
                if not is_thought:
                    response_answer.content += f"{thought_content}\n"
                    response_thinking.metadata["status"] = "done"
                    response_thinking.metadata["duration"] = time.time() - start_time
                    response_thinking.metadata["title"] = "已完成推理"
                    break
                elif thought_interrupt:
                    response_answer.content += f"{thought_content}\n"
                    response_thinking.metadata["status"] = "done"
                    response_thinking.metadata["duration"] = time.time() - start_time
                    response_thinking.metadata["title"] = "推理被中断"
                else:
                    response_thinking.content += f"- {thought_role}: {thought_content}\n"
                    response_thinking.metadata["duration"] = time.time() - start_time

        responses = []
        if response_thinking.content != '':
            responses.append(response_thinking)
        if response_answer.content != '':
            responses.append(response_answer)
        if len(responses) > 0:
            yield responses

        if thought_interrupt:
            break



if __name__ == '__main__':
    from pylib.ai.flow import Flow, Node, END, HumanNode

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
            super().__init__()
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
    human = HumanNode(verify_args=['1', '2'])

    START >> web >> n1 >> check('positive') >> subtract3 >> check('negative') >> human >> END

    web = webUI(START)
    # web.set_message_transformer(message_to_markdown)
    # web.set_message_transformer(message_to_markdown_with_thinking)
    web.launch()