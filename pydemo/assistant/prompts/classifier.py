

_TEMPLATE = '''\
System Instruction:
There are 5 categories of entities in a PowerPoint presentation: text, image, shape, slide,presentation. You need to perform the following tasks:
1. Categorize a given sentence into entity categories. Each sentence can have more than one category.
2. Classify whether a sentence requires context. Context is required when additional information about the
content of a presentation is required to fulfill the task described in the sentence.
- Adding an image about a given topic does not require context.
- Adding new text needs context to decide where to place the text on the current slide.

Let’s think step by step. Here are some examples:

{examples}

User: {query}
Assistant:'''


from prompts.prompts import DBPrompt

class Classifier(DBPrompt):
    def __init__(self, llm, db):
        super().__init__(llm, _TEMPLATE, db, 'examples', 'query')

    def __call__(self, query):
        return self.run(query=query)

    def init_for_test(self):
        self.insert_db_item('Make the title text on this slide red.', '''\
User: Make the title text on this slide red.
Assistant:
Categories: text
Thoughts: We can select the title text and make it red without knowing the existing text properties. Therefore we do not need context.
RequiresContext: false
''')

        self.insert_db_item('Add text that’s a poem about the life of a high school student with emojis.', '''\
User: Add text that’s a poem about the life of a high school student with emojis.
Assistant:
Categories: text
Thoughts: We need to know whether there is existing text on the slide to add the new poem. Therefore we need context.
RequiresContext: true
''')  
