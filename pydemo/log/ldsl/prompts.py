from langchain.prompts import PromptTemplate

from typing import Any

from langchain.vectorstores.base import VectorStore
# from langchain.docstore.document import Document

from langchain.schema.language_model import BaseLanguageModel, LanguageModelInput

class Prompt:
    def __init__(self, llm:BaseLanguageModel, template):
        self.prompt = PromptTemplate.from_template(template)
        self.llm  = llm
        pass

    def run(self, **kwargs: Any):
        input = self.prompt.format(**kwargs)
        output = self.llm.invoke(input)
        return output

    def __call__(self, **kwargs: Any):
        return self.run(**kwargs)


class DBPrompt(Prompt):
    def __init__(self, llm, template,
                db: VectorStore,
                db_value_key,
                db_query_key,
                db_search_k = 3,
                ):
        super().__init__(llm, template)
        self.db = db
        self.db_value_key = db_value_key
        self.db_query_key = db_query_key
        self.db_search_k = db_search_k

    def insert_db_item(self, text, value):
        metadata = { self.db_value_key: value }
        self.db.add_texts(texts=[text], metadatas=[metadata])

    def run(self, **kwargs: Any):
        if self is not None:
            query = kwargs[self.db_query_key]
            docs = self.db.similarity_search(query, k=self.db_search_k)

            value = [doc.metadata[self.db_value_key] for doc in docs]
            value = '/n'.join(value)
            kwargs[self.db_value_key]= value
        return super().run(**kwargs)    

    def __call__(self, **kwargs: Any):
        return self.run(**kwargs)


