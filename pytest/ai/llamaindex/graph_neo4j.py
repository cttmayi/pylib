# For OpenAI

import os

# os.environ["OPENAI_API_KEY"] = "API_KEY_HERE"

import logging
import sys
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# define LLM
llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
Settings.llm = llm
Settings.chunk_size = 512


from llama_index.core import KnowledgeGraphIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.graph_stores.neo4j import Neo4jGraphStore


from llama_index.llms.openai import OpenAI
from IPython.display import Markdown, display


documents = SimpleDirectoryReader(
    "dataset/txt"
).load_data()


username = os.environ.get("NEO4J_USERNAME", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "neo4j")
url = "bolt://127.0.0.1:7687"
database = "neo4j"


graph_store = Neo4jGraphStore(
    username=username,
    password=password,
    url=url,
    database=database,
)

storage_context = StorageContext.from_defaults(graph_store=graph_store)

# NOTE: can take a while!
index:KnowledgeGraphIndex = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    max_triplets_per_chunk=2,
)

from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine
query_engine:RetrieverQueryEngine = index.as_query_engine(
    include_text=False, response_mode="tree_summarize", verbose=True
)

response = query_engine.query("什么是Aigc")

print(response)