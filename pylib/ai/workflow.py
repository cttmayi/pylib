import warnings, copy, time

class BaseNode:
    def __init__(self): 
        self.params = {}
        self.successors = {}

    def set_params(self, params): 
        self.params = params

    def add_successor(self,node,action="default"):
        if action in self.successors: 
            raise Exception(f"Overwriting successor for action '{action}'")
        self.successors[action]=node;return node

    def prep(self,shared): pass
    def exec(self,prep_res): pass
    def post(self,shared,prep_res,exec_res): pass

    def _exec(self,prep_res): 
        return self.exec(prep_res)

    def _run(self,shared): 
        p = self.prep(shared)
        e = self._exec(p)
        return self.post(shared,p,e)

    def run(self,shared): 
        if self.successors: 
            raise Exception("Node won't run successors. Use Flow.")  
        return self._run(shared)

    def __rshift__(self,other): 
        return self.add_successor(other)

    def __sub__(self,action):
        if isinstance(action,str): 
            return _ConditionalTransition(self,action)
        raise TypeError("Action must be a string")

class _ConditionalTransition:
    def __init__(self, src:BaseNode, action:str): 
        self.src = src
        self.action = action

    def __rshift__(self,tgt): 
        return self.src.add_successor(tgt,self.action)

class Node(BaseNode):
    def __init__(self, max_retries=1, wait=0): 
        super().__init__()
        self.max_retries, self.wait = max_retries, wait

    def exec_fallback(self,prep_res,exc): 
        raise exc

    def _exec(self,prep_res):
        for self.cur_retry in range(self.max_retries):
            try: 
                return self.exec(prep_res)
            except Exception as e:
                if self.cur_retry == self.max_retries-1: 
                    return self.exec_fallback(prep_res,e)
                if self.wait > 0: 
                    time.sleep(self.wait)


class Flow:
    def __init__(self, start, params={}): 
        self.start = start
        self.params = params

    def get_next_node(self, curr:BaseNode, action:str):
        nxt = curr.successors.get(action or "default")
        if not nxt and curr.successors: 
            warnings.warn(f"Flow ends: '{action}' not found in {list(curr.successors)}")
        return nxt

    def run(self, shared):
        curr:BaseNode = copy.copy(self.start)
        p = self.params
        while curr: 
            curr.set_params(p)
            c = curr._run(shared)
            yield curr, c
            curr = copy.copy(self.get_next_node(curr, c))



if __name__ == '__main__':
    class NumberNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def prep(self, shared_storage):
            shared_storage['current'] = self.number

    class AddNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def prep(self, shared_storage):
            shared_storage['current'] += self.number

    class MultiplyNode(Node):
        def __init__(self, number):
            super().__init__()
            self.number = number

        def prep(self, shared_storage):
            shared_storage['current'] *= self.number

    class CheckPositiveNode(Node):
        def post(self, shared_storage, prep_result, proc_result):
            if shared_storage['current'] >= 0:
                return 'positive'
            else:
                return 'negative'

    class NoOpNode(Node):
        def prep(self, shared_storage):
            # Do nothing, just pass
            pass

    shared_storage = {}
    n1 = NumberNode(10)
    check = CheckPositiveNode()
    subtract3 = AddNode(-3)
    no_op = NoOpNode()  # Dummy node for the 'negative' branch

    # Build the cycle:
    #   n1 -> check -> if 'positive': subtract3 -> back to check
    n1 >> check
    check - 'positive' >> subtract3
    subtract3 >> check  
    # Attach a no-op node on the negative branch to avoid warning
    check - 'negative' >> no_op

    pipeline = Flow(start=n1)

    for _, _ in pipeline.run(shared_storage):
        continue

    # final result should be -2: (10 -> 7 -> 4 -> 1 -> -2)
    assert shared_storage['current'] == -2
    print('Done!')