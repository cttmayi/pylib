"""Beth's contributor service file.

Beth builds her QueryEngine and exposes it behind the standard
LlamaIndex Network Contributor Service. 

NOTE: Bob would probably make use of Docker and cloud 
compute services to make this production grade.
"""

from llama_index.networks.contributor import ContributorService
import uvicorn

from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex

documents = SimpleDirectoryReader("dataset/txt").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
#print(query_engine)


#response = query_engine.query("What is AIGC?")
#print(response)





beth_query_engine = query_engine
beth_contributor_service = ContributorService.from_config_file(
    ".env",  # settings/secrets for the service
    beth_query_engine
)


if __name__ == "__main__":
    uvicorn.run(beth_contributor_service.app, port=8000)