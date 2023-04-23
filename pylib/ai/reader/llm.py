import os

import time
import openai
from colorama import Fore
from pprint import pprint


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = 'http://47.251.11.225:8080/v1'


# Overly simple abstraction until we create something better
# simple retry mechanism when getting a rate error or a bad gateway
def create_chat_completion(messages, model=None, temperature=0.1, max_tokens=None)->str:
    """Create a chat completion using the OpenAI API"""
    response = None
    num_retries = 5

    for attempt in range(num_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            break
        except openai.error.RateLimitError:
            print("Error: ", "API Rate Limit Reached. Waiting 20 seconds...")
            time.sleep(20)
        except openai.error.APIError as e:
            if e.http_status == 502:
                print("Error: ", "API Bad gateway. Waiting 20 seconds...")
                time.sleep(20)
            else:
                raise
            if attempt == num_retries - 1:
                raise

    if response is None:
        raise RuntimeError("Failed to get response after 5 retries")
    
    # pprint(response)
    return response.choices[0].message["content"]
