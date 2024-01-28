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


human = HumanInputTool()

repl_tool = Tool(
    name="human",
    description="一个人类工具，有任何疑问，调用工具可以输出你的问题，此工具会进行答复，一次只问一个问题",
    func=human.run
)

from langchain.tools import format_tool_to_openai_function

tools = [repl_tool]
functions = [format_tool_to_openai_function(t) for t in tools]



PROMPT = """\
Given the function name and source code, generate an English language explanation of the function.
Function Name: {function_name}
Source Code:
{source_code}
Explanation:
"""

template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "你是一个信息收集者，需要收集报告写作的各种咨询（报告的主题和对象），并用makedown格式输出"
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

def ask(llm, title):

    inputs = template.format_messages(text=title)

    # inputs = []
    inputs.append(HumanMessage(content='你需要篇报告，写之前你需要了解主题，报告的对象是谁，掌握这些信息后，再进行写作'))
    print(inputs)
    output = llm.predict_messages(inputs, functions=functions)
    kwargs = output.additional_kwargs

    while kwargs.get("function_call"):
        function_name = kwargs["function_call"]["name"]
        function_arg1 = json.loads(kwargs["function_call"] ["arguments"]).get("__arg1")
        function_response = human.run( function_arg1 )

        inputs.append(FunctionMessage(name=function_name, content=function_response))

        output = llm.predict_messages(inputs, functions=functions)
        kwargs = output.additional_kwargs

    return output.content

if __name__ == '__main__':
    llm = ChatOpenAI(model="gpt-3.5-turbo-0613")
    ret = ask(llm, '写周报')
    print(ret)
    