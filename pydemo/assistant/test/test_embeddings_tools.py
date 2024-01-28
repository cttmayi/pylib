from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re


# Define which tools the agent can use to answer user queries
search = SerpAPIWrapper()
search_tool = Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    )


def fake_func(inp: str) -> str:
    return "foo"
fake_tools = [
    Tool(
        name=f"foo-{i}", 
        func=fake_func, 
        description=f"a silly function that you can use to get more information about the number {i}"
    ) 
    for i in range(99)
]
ALL_TOOLS = [search_tool] + fake_tools

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document


docs = [Document(page_content=t.description, metadata={"index": i}) for i, t in enumerate(ALL_TOOLS)]
 
vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())


retriever = vector_store.as_retriever()
 
def get_tools(query):
    docs = retriever.get_relevant_documents(query)
    return [ALL_TOOLS[d.metadata["index"]] for d in docs]

for tool in get_tools("whats the weather?"):
    print (tool)