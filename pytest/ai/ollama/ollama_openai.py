from openai import ChatCompletion
import openai

api_base = 'http://localhost:11434/v1'
api_key = 'your_api_key'

openai.api_base = api_base
openai.api_key = api_key


respense = ChatCompletion.create(
    model='llama2',
    messages=[
        {'role': 'user', 'content': 'Why is the sky blue?'}
    ],
)

print(respense)