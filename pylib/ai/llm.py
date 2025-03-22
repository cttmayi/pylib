from litellm import completion
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")

class LLM:
    def __init__(self, cfg, systmem_prompt= None):
        self.model = cfg.get('model', 'openai/gpt-4o')
        self.api_key = cfg.get('api_key')
        if self.api_key is None:
          raise Exception("api_key is required")
        self.system_prompt = systmem_prompt
        self.reset()

    def reset(self):
      self.messages = []
      if self.system_prompt is not None:
        self.messages.append({ "content": self.system_prompt,"role": "system"})

    def __call__(self, prompt):
      self.messages.append({ "content": prompt,"role": "user"})
      response = completion(
        model=self.model,
        messages=self.messages,
      )
      self.messages.append({ "content": response,"role": "assistant"})
      return response
    

## set ENV variables
os.environ["OPENAI_API_KEY"] = "your-api-key"

response = completion(
  model="openai/gpt-4o",
  messages=[{ "content": "Hello, how are you?","role": "user"}]
)
