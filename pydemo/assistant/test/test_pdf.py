from langchain.document_loaders import PyPDFLoader

import os
import getpass


loader = PyPDFLoader("test/data/Reflexion.pdf")
pages = loader.load_and_split()


from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
docs = faiss_index.similarity_search("what is reflexion?", k=2)
for doc in docs:
    print(str(doc.metadata["page"]) + ":", doc.page_content[:300])
