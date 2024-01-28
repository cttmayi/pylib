from langchain.memory import ConversationKGMemory
from langchain.llms import OpenAI


llm = OpenAI(temperature=0)
memory = ConversationKGMemory(llm=llm)
memory.save_context({"input": "say hi to sam"}, {"ouput": "who is sam"})
memory.save_context({"input": "sam is a friend"}, {"ouput": "okay"})

r = memory.load_memory_variables({"input": 'who is sam'})

print(r)