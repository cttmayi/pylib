from langchain.chat_models import ChatOpenAI
 
from dataclasses import dataclass, field

@dataclass
class ModelInfo:
    """Struct for model information.

    Would be lovely to eventually get this directly from APIs, but needs to be scraped from
    websites for now.
    """

    name: str
    max_tokens: int
    prompt_token_cost: float
    completion_token_cost: float


OPEN_AI_CHAT_MODELS = {
    info.name: info
    for info in [
        ModelInfo(
            name="gpt-3.5-turbo-0301",
            prompt_token_cost=0.0015,
            completion_token_cost=0.002,
            max_tokens=4096,
        ),
        ModelInfo(
            name="gpt-3.5-turbo-0613",
            prompt_token_cost=0.0015,
            completion_token_cost=0.002,
            max_tokens=4096,

        ),
        ModelInfo(
            name="gpt-3.5-turbo-16k-0613",
            prompt_token_cost=0.003,
            completion_token_cost=0.004,
            max_tokens=16384,
        ),
        ModelInfo(
            name="gpt-4-0314",
            prompt_token_cost=0.03,
            completion_token_cost=0.06,
            max_tokens=8192,
        ),
        ModelInfo(
            name="gpt-4-0613",
            prompt_token_cost=0.03,
            completion_token_cost=0.06,
            max_tokens=8191,
        ),
        ModelInfo(
            name="gpt-4-32k-0314",
            prompt_token_cost=0.06,
            completion_token_cost=0.12,
            max_tokens=32768,
        ),
        ModelInfo(
            name="gpt-4-32k-0613",
            prompt_token_cost=0.06,
            completion_token_cost=0.12,
            max_tokens=32768,
        ),
    ]
}


llm = ChatOpenAI()




if __name__ == '__main__':
    from langchain.prompts import (
        ChatPromptTemplate,
        HumanMessagePromptTemplate
    )

    from langchain.schema import HumanMessage

    #human_message_prompt = HumanMessagePromptTemplate.from_template('move file to folder')

    # chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])


    #r = llm.predict_messages([HumanMessage(content="move file foo to bar")])
    ret = llm.predict('tell me a joke')
    print(ret)

from langchain.chat_models.human import HumanInputChatModel