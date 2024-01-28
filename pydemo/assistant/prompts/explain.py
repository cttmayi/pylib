


_TEMPLATE = '''\
Contents: "{selection}"
Please create a comprehensive explanation in {lang} following the format below:

<Basic Definition/Main Idea>: <For the contents, if it's a word/concept, provide a concise definition; If it's a paragraph, briefly summarize the main point.>

<Real-Life Example or Analogy>: <Provide a real-life example or analogy related to everyday life to aid understanding of the contents>

<Summary>: <A one-sentence summary, highlighting the main point of understanding of the contents>'''


_LANG = 'chinese'

from prompts.prompts import Prompt


class Explain(Prompt):
    def __init__(self, llm, lang=_LANG):
        super().__init__(llm, _TEMPLATE)
        self._lang = lang

    def __call__(self, selection):
        return self.run(selection=selection , lang=self._lang)