from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import OpenAI

model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.0)


# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

    # You can add custom validation logic easily with Pydantic.
    @validator("setup")
    def question_ends_with_question_mark(cls, field):
        if field[-1] != "?":
            raise ValueError("Badly formed question!")
        return field


# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    # template="Answer the user query.\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    
)

print(parser.get_format_instructions())

# And a query intended to prompt a language model to populate the data structure.
prompt_and_model = prompt | model
prompt_and_model_parser = prompt | model
# output = prompt_and_model.invoke({"query": "Tell me a joke."})
# ret = parser.invoke(output)
#print('----------')
#print(type(output), output)
#print(type(ret), ret)

ret = prompt_and_model_parser.invoke({"query": "Tell me a joke."})
print('----------')
print(type(ret), ret)