
from langchain.chains.question_answering import load_qa_chain


_TEMPLATE = '''\
Answer this following question and respond in the {lang} language: """{selection}""" Do not wrap responses in quotes.'''


_LANG = 'chinese'

from prompts.prompts import Prompt, DBPrompt


class Question(Prompt):
    def __init__(self, llm, lang=_LANG):
        super().__init__(llm, _TEMPLATE)
        self._lang = lang

    def __call__(self, selection):
        return self.run(selection=selection, lang=self._lang)
    

_TEMPLATE_DB = '''\
Answer this following question and respond in the {lang} language: """{selection}""" Do not wrap responses in quotes.

{contents}

User: {query}
Assistant:
'''


from prompts.prompts import DBPrompt

class DBQuestion(DBPrompt):
    def __init__(self, llm, db):
        super().__init__(llm, _TEMPLATE_DB, db, 'contents', 'query')

    def __call__(self, query):
        return self.run(query=query)