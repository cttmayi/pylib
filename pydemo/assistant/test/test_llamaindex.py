


from llama_index import SimpleDirectoryReader

documents = SimpleDirectoryReader('./test_data').load_data()

from llama_index import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)


query_engine = index.as_query_engine()
response = query_engine.query("综合实力全球第五的AI大模型是哪个？")
print(response)