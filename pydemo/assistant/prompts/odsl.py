
_TEMPLATE = '''\
System instruction: ODSL is a DSL for performing actions in PowerPoint.
Here are examples of ODSL’s syntax:
# Get the title from all slides in the presentation
textRanges = select_text(scope="Presentation", name="Title")
# Gets the textRanges matching the string "Hello" from the provided shapes.
textRanges = select_text(scope=shapes, text="Hello")
# Formats the text in textRanges to be bold, italic, have Times New Roman font, have a
single underline, have font size 24, have the color teal and be Left aligned.
format_text(textRanges=textRanges, bold=true, fontName="Times New Roman",
horizontalAlignment="Left", size=24, color="teal", italic=true, underline="Single")
# Many of the argument to format statements are optional. For example, this format statement
makes the text bulleted and changes its color to olive.
format_text(textRanges=textRanges, bulleted=true, color="#808000")


Generate an ODSL program to fulfill the given user utterance. Remember to follow the followingrules when generating ODSL:
– For select_text, if scope is provided it must be a either Presentation or a variable of type shapes or slides. If no scope is provided, we select the user slide selection.
– You must select or insert an entity before formatting or deleting it.
– Never use for loops, array indexing or if/else statements.

{examples}

User: {query}
Assistant:
'''


from prompts.prompts import DBPrompt

class ODSL(DBPrompt):
    def __init__(self, llm, db):
        super().__init__(llm, _TEMPLATE, db, 'examples', 'query')

    def __call__(self, query):
        return self.run(query=query)

    def init_for_test(self):
        self.insert_db_item('Change the text format to make it look like a typewriter', '''\
User: Change the text format to make it look like a typewriter
Assistant:
text = select_text()
format_text(textRanges=text, fontName="Courier New", size=18, bold=false, italic=false,
underline="None", color="#000000", bulleted=false, horizontalAlignment="Left")
''')

        self.insert_db_item('Change the text format to make it look elegant', '''\
User: Change the text format to make it look elegant
Assistant:
text = select_text()
format_text(textRanges=text, fontName="Times New Roman", size=18, italic=true)
''')  
    

