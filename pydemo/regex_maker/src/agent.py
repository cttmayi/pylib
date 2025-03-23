from pylib.basic.print import print_truncated, print_blue, print_green



class Message:
    def __init__(self, to_role, prompt, data, from_role, new_task=False):
        self.to_role = to_role
        self.from_role = from_role
        self.prompt = prompt
        self.data = data
        self.new_task = new_task


class Agent:
    def __init__(self):
        self.name = None

    def set_name(self, name):
        self.name = name

    # input: prompt, data, from_role
    # output: prompt, data, to_role
    def chat(self, prompt, data, from_role):
        raise NotImplementedError
        
    def status(self):
        raise NotImplementedError

    def _message(self, to_role, prompt='', data=None, new_task=False):
        return Message(to_role, prompt, data, self.name, new_task=new_task)
    
    def message_new_task(self, to_role, prompt='', data=None):
        return self._message(to_role, prompt, data, new_task=True)
    
    def message_reply(self, to_role, prompt, data=None):
        return self._message(to_role, prompt, data)
    
    def message_end(self):
        return self._message(None)


class Router:
    ROUTER_NAME = 'Router'

    PROMPT_TASK_START = '请开始你的任务'

    def __init__(self, verbose=False):
        self.agents = {}
        self.user_name = None
        self.verbose = verbose
    
    def route(self, agent_name, prompt, data, from_role, new_task):
        agent:Agent = self.agents[agent_name]
        return agent.chat(
            prompt, data=data, from_role=from_role, new_task=new_task)

    def add_agent(self, agent_name, agent:Agent):
        if agent_name not in self.agents:
            self.agents[agent_name] = agent
            agent.set_name(agent_name)
            if self.user_name is None:
                self.user_name = agent_name

    def status(self):
        agent:Agent = self.agents[self.user_name]
        agent.status()

    def run(self):
        prompt = self.PROMPT_TASK_START
        data = None
        to_role = self.user_name
        from_role = self.ROUTER_NAME
        new_task = True

        while(to_role is not None):
            if self.verbose:
                print_green(f'{from_role}', end='')
                print_blue(r' say to ', end='')
                print_green(f'{to_role}', end='')
                print_blue(':')
                print_truncated(f'\t{prompt}')
            message: Message = self.route(to_role, prompt, data, from_role, new_task)
            from_role = to_role
            prompt, data, to_role, new_task = message.prompt, message.data, message.to_role, message.new_task

        # self.status()