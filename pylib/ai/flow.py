import warnings, copy, time, types


class NodeMessage:
    def __init__(self, **kwargs):
        self.content = None
        self.start = False
        self.end = False
        self.next_action = None
        self.next_node = None
        self.data = None
        self.curr_node = None
        self.order = 0
        self.set(**kwargs)

    def set(self, **kwargs):
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k,v)

    def to_dict(self):
        ret = {}
        ret['role'] = self.curr_node.name
        ret['content'] = self.content
        return ret


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

    def execute(self, shared, params): return params
    def if_cond(self, shared, params): pass

    def _node_message(self, exec_yield):
        if exec_yield is None:
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
    def __init__(self, name=None): 
        super().__init__(name)


class Flow(_BaseNode):
    def __init__(self, name='assistant'):
        super().__init__(name='Start')
        self.role = name

    def execute(self, shared, params):
        yield str(params)
        return params

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
        order = 0
        messages = []
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
                        message.set(curr_node=curr_node, start=start, order=order)
                        start = False
                        ret = yield messages + [message.to_dict()]
                        if ret is not None:
                            iter.send(ret)
                except StopIteration as e:
                    next_action, exec_ret = self._get_exec_ret(e.value)
            else:
                next_action, exec_ret = self._get_exec_ret(iter)

            next_action = next_action or curr_node.if_cond(shared, params)

            next_node = copy.copy(self._get_next_node(curr_node, next_action))
            params = exec_ret

            message:NodeMessage = curr_node._node_message(exec_item)
            message.set(curr_node=curr_node, next_action=next_action, next_node=next_node, start=start, end=True, order=order)
            messages += [message.to_dict()]
            yield messages
            order += 1


class HumanNode(_BaseNode):
    def __init__(self): 
        super().__init__(name='Human')

    def execute(self, shared, params):
        text = yield ''
        yield text
        yield text
        return {'text': text, 'params': params}

class _EndNode(_BaseNode):
    def __init__(self):
        super().__init__(name='End')

    def execute(self, shared, params):
        yield str(params)
        return params

    def add_successor(self, node, action="default"):
        raise Exception(f"{self.name} can't add successor '{node.__class__.__name__}' for action '{action}'")


END = _EndNode()


if __name__ == '__main__':
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
    HUMAN = HumanNode()

    n1 = NumberNode(10)
    check = CheckPositiveNode()
    subtract3 = AddNode(-3)

    START >> n1 >> check('positive') >> subtract3 >> check('negative')  >> HUMAN >> END

    iter_= START.run(shared_storage)


    pos = 0
    while(True):
        try:
            messages = next(iter_)
            pr = []
            for message in messages:
                text = f"{message['role']}: {message['content'] or ''}"
                pr.append(text)
            # pr_text = '\n'.join(pr)
            # print(pr_text[pos:], end='', flush=True)
            print(pr[-1])
            pos = len(pr)
            # print(message)
            interrupt = message['role'] == 'Human' and message['content'] == ''
            if interrupt:
                humun_input = input(message['role'] + ':')
                iter_.send(humun_input)
        except StopIteration as e:
            break

    print()

    # final result should be -2: (10 -> 7 -> 4 -> 1 -> -2)
    assert shared_storage['current'] == -2, f"Expected -2, got {shared_storage['current']}"
