from IPython import get_ipython
from typing_extensions import Annotated

import autogen
from autogen.cache import Cache

config_list = autogen.config_list_from_json(
    "config/gen/OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
    },
)

llm_config = {
    "config_list": config_list,
    "timeout": 120,
}

chatbot = autogen.AssistantAgent(
    name="chatbot",
    # system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)


# define functions according to the function description

with Cache.disk() as cache:
    # start the conversation
    user_proxy.initiate_chat(
        chatbot,
        message="Draw two agents chatting with each other with an example dialog.",
        cache=cache,
    )