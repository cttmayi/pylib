from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import Tool
from langchain.utilities import PythonREPL
python_repl = PythonREPL()
# You can create the tool to pass to an agent
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run
)

model = ChatOpenAI(model="gpt-3.5-turbo-0613")
from langchain.tools import format_tool_to_openai_function

tools = [repl_tool]
functions = [format_tool_to_openai_function(t) for t in tools]
message = model.predict_messages([HumanMessage(content='Write a python code to eval 1 plus 1.')], functions=functions)

print(message.additional_kwargs['function_call'])