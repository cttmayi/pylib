import warnings, copy, time, types


class NodeMessage:
    def __init__(self, role=None, content=None, tool_calls=None, **kwargs):
        self.message = {'content': content, 'role': role, 'tool_calls': tool_calls}
        self.start = False
        self.end = False
        self.next_action = None
        self.next_node = None
        self.data = None
        self.curr_node = None
        self.set(**kwargs)

    def set(self, **kwargs):
        for k,v in kwargs.items():
            if k in self.message:
                self.message[k] = v
            elif k == 'curr_node':
                self.curr_node = v
                if self.message['role'] is None:
                    self.message['role'] = v.name
            elif hasattr(self, k):
                setattr(self, k,v)


class _BaseNode:
    def __init__(self, name): 
        self.name = name or self.__class__.__name__
        self.successors = {}

    def add_successor(self, node, action="default"):
        if action in self.successors: 
            raise Exception(f"{self.name} overwrite successor '{node.__class__.__name__}' for action '{action}'")
        if isinstance(node, _ConditionalTransition):
            self.successors[action] = node.src
        else:
            self.successors[action] = node
        return node

    def is_end(self): 
        return len(self.successors) == 0

    def execute(self, shared, params): return params
    def if_cond(self, shared, params): pass

    def _node_message(self, exec_yield):
        if isinstance(exec_yield, dict):
            return NodeMessage(curr_node=self, **exec_yield)
        elif exec_yield is None:
            return NodeMessage(curr_node=self)
        return NodeMessage(curr_node=self, content=str(exec_yield))

    def __rshift__(self, other): 
        return self.add_successor(other)

    def __sub__(self, action):
        if isinstance(action,str): 
            return _ConditionalTransition(self, action)
        raise TypeError("Action must be a string")
    
    def __call__(self, action):
        return self.__sub__(action)


class _ConditionalTransition:
    def __init__(self, src:_BaseNode, action:str): 
        self.src = src
        self.action = action

    def __rshift__(self,tgt): 
        return self.src.add_successor(tgt, self.action)


class Node(_BaseNode):
    def __init__(self, name=None, verbose=False): 
        super().__init__(name)
        self.verbose = verbose


class StartNode(_BaseNode):
    def __init__(self):
        super().__init__(name='START')

    def _get_next_node(self, curr:_BaseNode, action:str):
        nxt = curr.successors.get(action or "default")
        if not nxt and curr.successors: 
            warnings.warn(f"Flow ends: '{action}' not found in {list(curr.successors)}")
        return nxt

    def _get_exec_ret(self, exec_ret):
        if isinstance(exec_ret, tuple) and len(exec_ret) == 2:
            return exec_ret[0], exec_ret[1]
        return None, exec_ret

    def run(self, shared={}, params=None):
        curr_node:_BaseNode = None
        next_node:_BaseNode = copy.copy(self)
        while next_node:
            curr_node = next_node
            iter = curr_node.execute(shared, params)
            start = True
            exec_item = None
            if isinstance(iter, types.GeneratorType):
                try:
                    while True:
                        exec_item = next(iter)
                        message:NodeMessage = curr_node._node_message(exec_item)
                        message.set(curr_node=curr_node, start=start)
                        start = False
                        yield message
                except StopIteration as e:
                    next_action, exec_ret = self._get_exec_ret(e.value)
            else:
                next_action, exec_ret = self._get_exec_ret(iter)

            next_action = next_action or curr_node.if_cond(shared, params)

            next_node = copy.copy(self._get_next_node(curr_node, next_action))
            params = exec_ret

            exec_item = exec_item or exec_ret
            message:NodeMessage = curr_node._node_message(exec_item)
            message.set(curr_node=curr_node, next_action=next_action, next_node=next_node, start=start, end=True)
            yield message


class EndNode(_BaseNode):
    def __init__(self):
        super().__init__(name='END')

    def execute(self, shared, params):
        yield params


def message_to_gradio_markdown(node_message_iter):
    content = "# Flow\n"
    for node_message in node_message_iter:
        message = node_message.message
        if node_message.start:
            content += f"{message['role']}: "
        if node_message.start == False and node_message.end == False:
            content += "... "
        if node_message.end:
            content += f"{message['content']}\n" if message['content'] is not None else "\n"
        yield content

def message_to_gradio_chatmessage(node_message_iter):
    from gradio import ChatMessage
    start_time = time.time()
    response = ChatMessage(
        role="assistant",
        content="",
        metadata={"title": "Thinking step-by-step", "id": 0, "status": "pending"}
    )
    yield response

    accumulated_thoughts = ""
    for node_message in node_message_iter:
        thought = node_message.message['content']
        accumulated_thoughts += f"- {thought}\n\n"
        response.content = accumulated_thoughts.strip()
        yield response

    response.metadata["status"] = "done"
    response.metadata["duration"] = time.time() - start_time
    yield response

    response = [
        response,
        ChatMessage(
            role="assistant",
            content= node_message.message['content']
        )
    ]
    yield response


if __name__ == '__main__':
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
    START = StartNode()
    END = EndNode()
    n1 = NumberNode(10)
    check = CheckPositiveNode()
    subtract3 = AddNode(-3)

    START >> n1 >> check('positive') >> subtract3 >> check('negative')  >> END

    iter_= START.run(shared_storage)

    if False:
        iter_= START.run(shared_storage)
        pos = 0
        for message in message_to_graido_string(iter_):
            print(message[pos:], end='', flush=True)
            pos = len(message)

        # final result should be -2: (10 -> 7 -> 4 -> 1 -> -2)
        assert shared_storage['current'] == -2, f"Expected -2, got {shared_storage['current']}"
    else:
        import gradio as gr
        def echo(message, history):
            text = message['text']
            file = message.get('file')
            iter_= START.run(shared_storage, params=len(text))
            for msg in message_to_gradio_chatmessage(iter_):
                yield msg

        with gr.Blocks(fill_height=True) as demo:
            gr.ChatInterface(
                fn=echo, 
                type="messages",
                multimodal=True,
                textbox=gr.MultimodalTextbox(file_count="multiple"),
            )
        demo.launch()