from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore = Chroma("langchain_store", embeddings)

ltext = [
    'hi',
    'how are you',
    'thank you'
]

vectorstore.add_texts(texts=ltext)

r = vectorstore.similarity_search('hello')

print(r)