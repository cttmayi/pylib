
from langchain import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}."
)
s = prompt_template.format(adjective="funny", content="chickens")

print(s)