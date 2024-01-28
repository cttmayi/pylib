from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

model = ChatOpenAI(model="gpt-3.5-turbo-0613")
from langchain.tools import ShellTool, format_tool_to_openai_function

tools = [ShellTool()]
functions = [format_tool_to_openai_function(t) for t in tools]
message = model.predict_messages([HumanMessage(content='count how many lines in a.txt?')], functions=functions)

print(message.additional_kwargs['function_call'])
