from langchain.document_loaders import OnlinePDFLoader


loader = OnlinePDFLoader("https://arxiv.org/pdf/2302.03803.pdf")

pages = loader.load()

from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
docs = faiss_index.similarity_search("How will the community be engaged?", k=2)
for doc in docs:
    print(str(doc.metadata["page"]) + ":", doc.page_content[:300])