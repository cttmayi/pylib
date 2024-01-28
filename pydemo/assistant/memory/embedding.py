from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

import os

from memory.memory import DB


class Embedding(DB):
    def __init__(self, name, embeddings=None, directory='./default_db'):
        if embeddings is None:
            embeddings = OpenAIEmbeddings()

        self.is_first = not os.path.exists(directory)
        self.vectorstore = Chroma(name, embeddings, persist_directory=directory)

    def add_texts(self, texts, metadatas=None):
        self.vectorstore.add_texts(texts=texts, metadatas=metadatas)

    def insert_items(self, dicts, key):
        texts = []
        metadatas = []
        for dict in dicts:
            texts.append(dict[key])
            metadatas.append(dict)
        # self.add_texts(texts, metadatas)
        self.vectorstore.add_texts(texts=texts, metadatas=metadatas)

    def search(self, text):
        ret = self.vectorstore.similarity_search(text)
        return ret


if __name__ == '__main__':
    ltext = [
        'hi',
        'how are you',
        'thank you'
    ]

    lmetadata = [
        {'values': 'haha'},
        {'value':'how to do'},
        {'value':'OK'}

    ]
    db = Embedding('default', directory='./chroma.db')
    if db.is_first:
        db.add_texts(ltext, lmetadata)
    print(db.search('hello'))
