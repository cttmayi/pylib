#import sys
#sys.path.append('..')
import json

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, FunctionMessage
from langchain.agents import Tool
from langchain.prompts.chat import HumanMessagePromptTemplate

from tools.tool_human import HumanInputTool

from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate


from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI



human = HumanInputTool()

repl_tool = Tool.from_function(
    name="human",
    description="一个人类工具，有任何疑问，调用工具可以输出你的问题，此工具会进行答复，一次只问一个问题",
    func=human.run
)


tools = [repl_tool]

def ask(llm, title):

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    agent.run("")

    return output.content

if __name__ == '__main__':
    llm = ChatOpenAI(model="gpt-3.5-turbo-0613")
    ret = ask(llm, '你是一个信息收集者，需要收集报告写作的各种咨询（报告的主题和对象），并用makedown格式输出')
    print(ret)
    