import os
import re
from openai import OpenAI

from pylib.basic.cache import cache_disk_for_class


MODELS = {
    "gpt-4": "openai/gpt-4",
    "qwen-plus": "qwen-plus",
    "qwen-max": "qwen-max",
}

_OPENAI_COMPATIBLIE_MODELS = [
    {
        "compatible_func": lambda x: x.startswith("qwen-"),
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key": os.environ.get("DASHSCOPE_API_KEY"),
    },
]

class LLM:
    def __init__(self, model, systmem_prompt= None, **kwargs):
        self._client = None
        self._model = MODELS.get(model, model)
        self._api_key = kwargs.get('api_key')
        self._api_base = kwargs.get('api_base')
        self._compatible_openai_model()
        self.system_prompt = systmem_prompt
        self.reset()


    def reset(self):
        self.messages = []
        if self.system_prompt is not None:
            self.messages.append({ "content": self.system_prompt,"role": "system"})


    def _compatible_openai_model(self):
        for compatible in _OPENAI_COMPATIBLIE_MODELS:
            compatible_func = compatible['compatible_func']
            if compatible_func(self._model):
                self._api_base = compatible['api_base']
                self._api_key = self._api_key if self._api_key else compatible['api_key']
                self._client = OpenAI(api_key=self._api_key, base_url=self._api_base)


    @cache_disk_for_class()
    def _completion(self, model, prompt, hashable_messages):
        messages = self.messages.copy()
        messages.append({ "content": prompt,"role": "user"})
        if self._client is not None:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                stream=False,
            )
            message = response.choices[0].message.content
            assistant = response.choices[0].message.role
        else:
            from litellm import completion
            response = completion(
                model=model,
                api_key=self._api_key,
                api_base=self._api_base,
                messages=messages,
                stream=False,
            )
            message = response['choices'][-1]['message']['content']
            assistant = response['choices'][-1]['message']['role']

        return message, assistant

    def __call__(self, prompt, chat=False):
        hashable_messages = tuple((msg["role"], msg["content"]) for msg in self.messages)
        content, assistant = self._completion(self._model, prompt, hashable_messages)
        if chat:
            self.messages.append({ "content": prompt,"role": "user"})
            self.messages.append({ "content": content,"role": assistant})
        return content
    
    def __hash__(self):
        return hash(self._model)


    def chat(self, prompt):
        return self.__call__(prompt, chat=True)

    # 内容提取器
    def content_filter(self, content):
        matches = re.findall(r'```(.*?)\n(.*?)\n```', content, re.DOTALL)
        if matches:
            results = []
            for match in matches:
                type = match[0].strip()
                content_ = match[1].strip()
                results.append({ 'type': type, 'content': content_})
            return results
        return None


if __name__ == '__main__':
    llm = LLM("qwen-max")
    prompt = "请帮我生成一个python代码，匹配以下字符串：\n\n"
    prompt += "1. 2023-10-01\n"
    message = llm(prompt)
    print("message:")
    print(message)
    print('code:')
    print(llm.content_filter(message))

    message = '''
```regex
^\d{4}-\d{2}-\d{2}$
```
```regex
^\d{4}-\d{2}-\d{2}$
```
'''
    regexs = llm.content_filter(message)
    print('regexs:')
    print(regexs)
