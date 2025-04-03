import warnings, copy, time

class _BaseNode:
    def __init__(self, name): 
        self.name = name or self.__class__.__name__
        self.params = {}
        self.successors = {}

    def set_params(self, params): 
        self.params = params

    def add_successor(self, node, action="default"):
        if action in self.successors: 
            raise Exception(f"{self.name} overwrite successor '{node.__class__.__name__}' for action '{action}'")
        if isinstance(node, _ConditionalTransition):
            self.successors[action] = node.src
        else:
            self.successors[action] = node
        return node

    def prep(self, shared): pass
    def exec(self, prep_res): pass
    def post(self, shared, prep_res, exec_res): pass

    def _exec(self,prep_res): 
        return self.exec(prep_res)

    def _run(self,shared): 
        p = self.prep(shared)
        e = self._exec(p)
        return self.post(shared, p, e)

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
    def __init__(self, name=None, max_retries=1, wait=0): 
        super().__init__(name)
        self.max_retries, self.wait = max_retries, wait

    def exec_fallback(self, prep_res, exc): 
        raise exc

    def _exec(self, prep_res):
        for self.cur_retry in range(self.max_retries):
            try: 
                return self.exec(prep_res)
            except Exception as e:
                if self.cur_retry == self.max_retries-1: 
                    return self.exec_fallback(prep_res,e)
                if self.wait > 0: 
                    time.sleep(self.wait)

    def _get_next_node(self, curr:_BaseNode, action:str):
        nxt = curr.successors.get(action or "default")
        if not nxt and curr.successors: 
            warnings.warn(f"Flow ends: '{action}' not found in {list(curr.successors)}")
        return nxt

    def run(self, shared={}, params={}):
        current_node:_BaseNode = copy.copy(self)
        while current_node:
            current_node.set_params(params)
            next_action = current_node._run(shared)
            yield current_node, next_action
            current_node = copy.copy(self._get_next_node(current_node, next_action))


END = Node(name="END")

if __name__ == '__main__':
    class NumberNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def prep(self, shared):
            shared['current'] = self.number

    class AddNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def prep(self, shared):
            shared['current'] += self.number

    class MultiplyNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def prep(self, shared):
            shared['current'] *= self.number

    class CheckPositiveNode(Node):
        def post(self, shared, prep_result, proc_result):
            if shared['current'] >= 0:
                return 'positive'
            else:
                return 'negative'

    shared_storage = {}
    n1 = NumberNode(10)
    check = CheckPositiveNode()
    subtract3 = AddNode(-3)

    n1 >> check('positive') >> subtract3 >> check('negative') >> END

    for curr, nxt in n1.run(shared_storage):
        if nxt is None:
            print(curr.name, end=' -> ')
        else:
            print(f'{curr.name}({nxt})', end=' -> ')
    print('DONE')

    # final result should be -2: (10 -> 7 -> 4 -> 1 -> -2)
    assert shared_storage['current'] == -2, f"Expected -2, got {shared_storage['current']}"