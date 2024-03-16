import autogen

llm_config = {
    "timeout": 600,
    "cache_seed": 44,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-3.5-turbo-0301"]},
    ),
    "temperature": 0,
}


# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "work_dir",
        "use_docker": False,
    },
)

task1 = """
Find arxiv papers that show how are people studying trust calibration in AI based systems
"""

user_proxy.initiate_chat(assistant, message=task1)


# task2 = "analyze the above the results to list the application domains studied by these papers "
# user_proxy.initiate_chat(assistant, message=task2, clear_history=False)


# task3 = """Use this data to generate a bar chart of domains and number of papers in that domain and save to a file
# """
# user_proxy.initiate_chat(assistant, message=task3, clear_history=False)