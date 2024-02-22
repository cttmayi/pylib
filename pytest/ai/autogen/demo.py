import autogen

from autogen.agentchat import AssistantAgent, UserProxyAgent
from autogen import config_list_from_json

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample.json
config_list = config_list_from_json(env_or_file="config/gen/OLLAMA_CONFIG_LIST")
print(config_list)
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}) # IMPORTANT: set to True to run code in docker, recommended
user_proxy.initiate_chat(assistant, message="Draw a rect")
# This initiates an automated chat between the two agents to solve the task


