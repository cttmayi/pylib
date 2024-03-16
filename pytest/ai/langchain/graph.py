# https://python.langchain.com/docs/use_cases/graph/integrations/graph_memgraph_qa

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


import os

from gqlalchemy import Memgraph
from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain.prompts import PromptTemplate
from langchain_community.graphs import MemgraphGraph
from langchain_openai import ChatOpenAI

username = os.environ.get("NEO4J_USERNAME", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "neo4j")


memgraph = Memgraph(host="127.0.0.1", port=7687, username=username, password=password)

# Creating and executing the seeding query
query = """
    MERGE (g:Game {name: "Baldur's Gate 3"})
    WITH g, ["PlayStation 5", "Mac OS", "Windows", "Xbox Series X/S"] AS platforms,
            ["Adventure", "Role-Playing Game", "Strategy"] AS genres
    FOREACH (platform IN platforms |
        MERGE (p:Platform {name: platform})
        MERGE (g)-[:AVAILABLE_ON]->(p)
    )
    FOREACH (genre IN genres |
        MERGE (gn:Genre {name: genre})
        MERGE (g)-[:HAS_GENRE]->(gn)
    )
    MERGE (p:Publisher {name: "Larian Studios"})
    MERGE (g)-[:PUBLISHED_BY]->(p);
"""

memgraph.execute(query)


graph = MemgraphGraph(url="bolt://localhost:7687", username=username, password=password)

graph.refresh_schema()


print(graph.schema)


chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0), graph=graph, verbose=True, model_name="gpt-3.5-turbo"
)

response = chain.run("Which platforms is Baldur's Gate 3 available on?")
print(response)