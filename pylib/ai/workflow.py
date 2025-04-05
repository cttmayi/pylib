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

    def execute(self, shared, params): pass
    def conditional(self, shared, exec_res): pass

    def node_message(self, shared, exec_res):
        if isinstance(exec_res, dict):
            return NodeMessage(curr_node=self, **exec_res)
        return NodeMessage(curr_node=self)

    def _exec(self, shared, params): 
        return self.execute(shared, params)

    def _run(self,shared, params):
        exec_iter = self._exec(shared, params)
        if exec_iter is not None:
            if isinstance(exec_iter, types.GeneratorType):
                for exec_ret in exec_iter: 
                    yield exec_ret
            else: 
                exec_ret = exec_iter
                yield exec_ret

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
        self.set_retries(1, 0)

    def set_retries(self, max_retries, wait=0):
        self.max_retries, self.wait = max_retries, wait
        self.curr_retry = 0

    def exec_fallback(self, exc): 
        raise exc

    def _exec(self, shared, params):
        for self.curr_retry in range(self.max_retries):
            try: 
                return self.execute(shared, params)
            except Exception as e:
                if self.curr_retry == self.max_retries - 1: 
                    return self.exec_fallback(e)
                if self.wait > 0: 
                    time.sleep(self.wait)


class StartNode(_BaseNode):
    def __init__(self):
        super().__init__(name='START')

    def _get_next_node(self, curr:_BaseNode, action:str):
        nxt = curr.successors.get(action or "default")
        if not nxt and curr.successors: 
            warnings.warn(f"Flow ends: '{action}' not found in {list(curr.successors)}")
        return nxt

    def run(self, shared={}, params=None):
        curr_node:_BaseNode = None
        next_node:_BaseNode = copy.copy(self)
        while next_node:
            curr_node = next_node
            iter = curr_node._run(shared, params)
            start = True
            try:
                while True:
                    exec_ret = next(iter)
                    message:NodeMessage = curr_node.node_message(shared, exec_ret)
                    message.set(curr_node=curr_node, start=start)
                    start = False
                    yield message
            except StopIteration as e:
                exec_ret = e.value

            # for exec_ret in iter:
            #     message:NodeMessage = self.node_message(shared, exec_ret)
            #     message.set(curr_node=curr_node, start=start)
            #     start = False
            #     yield message

            # next step
            next_action = curr_node.conditional(shared, exec_ret)
            next_node = copy.copy(self._get_next_node(curr_node, next_action))
            params = exec_ret

            message:NodeMessage = self.node_message(shared, exec_ret)
            message.set(curr_node=curr_node, next_action=next_action, next_node=next_node, start=start, end=True)
            yield message


class EndNode(_BaseNode):
    def __init__(self):
        super().__init__(name='END')

    def execute(self, shared, params):
        yield params





def message_thinking_answer(node_message_iter):
    content = ""
    for node_message in node_message_iter:
        message = node_message.message
        if node_message.start:
            content += f"\n\n{node_message.curr_node.name}:"
        if node_message.start == False and node_message.end == False:
            content += f"\n{node_message.curr_node.name}: {message['content']}"

        if node_message.end:
            content += f"\n{node_message.curr_node.name}: {message['content']}"
        yield content


if __name__ == '__main__':
    class NumberNode(Node):
        def __init__(self, number):
            super().__init__(verbose=True)
            self.number = number

        def execute(self, shared, params):
            shared['current'] = self.number

    class AddNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def execute(self, shared, params):
            current = shared['current']
            if self.number > 0:
                for _ in range(self.number):
                    current += 1
                    yield current
                    time.sleep(1)
            elif self.number < 0:
                for _ in range(abs(self.number)):
                    current -= 1
                    yield current
                    time.sleep(1)
            else:
                yield current
            
            shared['current'] = current

    class MultiplyNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def execute(self, shared, params):
            shared['current'] *= self.number
            yield shared['current']

    class CheckPositiveNode(Node):
        def conditional(self, shared, exec_res):
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

    if True:
        pos = 0
        for message in message_thinking_answer(iter_):
            print(message[pos:], end='', flush=True)
            pos = len(message)

        # final result should be -2: (10 -> 7 -> 4 -> 1 -> -2)
        assert shared_storage['current'] == -2, f"Expected -2, got {shared_storage['current']}"
    else:
        import gradio as gr
        def echo(message, history):
            for msg in message_thinking_answer(iter_):
                yield msg

        with gr.Blocks(fill_height=True) as demo:
            gr.ChatInterface(
                fn=echo, 
                type="messages",
            )
        demo.launch()