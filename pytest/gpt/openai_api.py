import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

import openai

api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key
openai.api_base = 'http://47.251.11.225:8080/v1' # 代理

# completion = openai.ChatCompletion.create(
#    model="gpt-3.5-turbo",
#    messages=[
#        {"role": "system", "content": "You are a helpful assistant."},
#        {"role": "user", "content": "Who won the world series in 2020?"},
#        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#        {"role": "user", "content": "Where was it played?"}
#    ]
# )

# print(completion.choices[0].message)

response = openai.Completion.create(engine="davinci", prompt="Hello world", max_tokens=50)
print(response)