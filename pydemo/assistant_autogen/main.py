from IPython import get_ipython
from typing_extensions import Annotated

import autogen
from autogen.cache import Cache

import prompt

from autogen.coding.embedded_ipython_code_executor import EmbeddedIPythonCodeExecutor


config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        # "model": ["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
        "model": ["gpt-4"],
    },
)

llm_config = {
    "config_list": config_list,
    "timeout": 120,
}






chatbot = autogen.AssistantAgent(
    name="chatbot",
    # system_message=prompt.system_prompt,
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
        # "executor": EmbeddedIPythonCodeExecutor(output_dir="coding")
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)


# define functions according to the function description

with Cache.disk() as cache:

    user_proxy.initiate_chat(
        chatbot,
        message="总结arXiv的最新的5篇文章",
        cache=cache,
    )


#@user_proxy.register_for_execution()
#@chatbot.register_for_llm(name="email info", description="get email address by name")
#def get_email_address(cell: Annotated[str, "name"]) -> str:
#    return 'ling.yuan@hotmail.com'

