from IPython import get_ipython
from typing_extensions import Annotated

import autogen
from autogen.cache import Cache



from autogen.coding.embedded_ipython_code_executor import EmbeddedIPythonCodeExecutor


config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
    },
)

llm_config = {
    "config_list": config_list,
    "timeout": 120,
}


system_prompt = """你是一个AI助理.
请理清如下需求需要使用哪些类函数， 工具有如下几类:
1. 邮件类函数
2. 查询类函数
3. 编译类函数
"""

system_prompt = """For email tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.
"""

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message=system_prompt,
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
        # "executor": EmbeddedIPythonCodeExecutor(output_dir="coding")
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)


# define functions according to the function description

with Cache.disk() as cache:
    user_proxy.initiate_chat(
        chatbot,
        message="把Autogen是一个好框架的消息邮件给Ling Yuan",
        cache=cache,
    )

@user_proxy.register_for_execution()
@chatbot.register_for_llm(name="email info", description="get email address by name")
def get_email_address(cell: Annotated[str, "name"]) -> str:
    print(cell)
    return 'ling.yuan@hotmail.com'