from langgraph.graph import StateGraph, MessageGraph, END

from typing import TypedDict, Annotated, Union, Sequence
from langchain_core.agents import AgentAction, AgentFinish
import operator

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Choose the LLM that will drive the agent
llm = ChatOpenAI(model="gpt-3.5-turbo")


prompt = ChatPromptTemplate.from_messages([
    # ("system", "你是一个科技作家， 按用户要求写一篇科技文章。你将会得到老师的反馈，一旦获得反馈，请重新在写一篇文章"),
    SystemMessage(content="你是一个科技作家， 按用户要求写一篇科技文章。你将会得到老师的反馈，一旦获得反馈，请重新在写一篇文章"),
    MessagesPlaceholder(variable_name="messages"),
])
writer = prompt | llm

r_prompt = ChatPromptTemplate.from_messages([
    # ("system", "你是一位老师，协助审核作家文章， 审核角度：长度，深度，风格等角度. 请提供修改建议， 如没有建议， 输出‘END’"),
    SystemMessage(content="你是一个老师，协助审核作家文章， 审核角度：长度，深度，风格等角度. 请提供修改建议， 如没有建议， 输出‘END’"),
    MessagesPlaceholder(variable_name="messages"),
])

reflection = r_prompt | llm

def generation_node(messages: Sequence[BaseMessage]):
    res = writer.invoke({'messages': messages})
    return res


def reflection_node(messages: Sequence[BaseMessage]):
    cls_map = {'ai': HumanMessage, 'human': AIMessage}
    translated = [messages[0]] + [
        cls_map[msg.type](content=msg.content) for msg in messages[1:]
    ]

    res = reflection.invoke({'messages': translated})
    return HumanMessage(content=res.content)


# Initialize the StateGraph with this state
graph = MessageGraph()
# Create nodes and edges
graph.add_node("writer", generation_node)
graph.add_node("reflection", reflection_node)
graph.set_entry_point("writer")


def should_refection(messages):
    message = messages[-1]
    if len(messages) > 10 or message.content.find('END') >= 0:
        return END
    return 'reflection'

graph.add_conditional_edges("writer",should_refection)

def should_writer(messages):
    message = messages[-1]
    if message.content.find('END') >= 0:
        return END
    return 'writer'

# graph.add_edge("reflection", "writer")
graph.add_conditional_edges("reflection",should_writer)

app = graph.compile()

# The inputs should be a dictionary, because the state is a TypedDict
inputs = [
   HumanMessage(content="请用中文介绍GPIO")
]
for s in app.stream(inputs):
    print('----start')
    print(list(s.keys())[0])
    print(list(s.values())[0].content)
    print("----end")