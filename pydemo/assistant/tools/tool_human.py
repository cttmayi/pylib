
from langchain.tools import HumanInputRun

class HumanInputTool(HumanInputRun):

    def __init__(self):
        super().__init__(input_func=self._get_single_input)

    def _get_input(self) -> str:
        print("Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == "q":
                break
            contents.append(line)
        return "\n".join(contents)

    def _get_single_input(self) -> str:
        print("Insert your text :", end='')
        line = input()
        return line


if __name__ == '__main__':
    from langchain.agents import initialize_agent
    from langchain.chat_models import ChatOpenAI
    from langchain.agents import AgentType

    llm = ChatOpenAI(temperature=0.0)

    tool = HumanInputTool()

    agent_chain = initialize_agent(
        [tool],
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    agent_chain.run("Download the langchain.com webpage and grep for all urls. Return only a sorted list of them. Be sure to use double quotes.")