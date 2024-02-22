import autogen
from autogen.agentchat.contrib.agent_builder import AgentBuilder

config_file_or_env = "config/gen/OAI_CONFIG_LIST"
llm_config = {"temperature": 0}
config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": ["gpt-4-1106-preview", "gpt-4"]})


def start_task(execution_task: str, agent_list: list):
    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list, **llm_config})
    agent_list[0].initiate_chat(manager, message=execution_task)


builder = AgentBuilder(
    config_file_or_env=config_file_or_env, builder_model="gpt-4-1106-preview", agent_model="gpt-4-1106-preview"
)

building_task = "Generate some agents that can find papers on arxiv by programming and analyzing them in specific domains related to computer science and medical science."

agent_list, agent_configs = builder.build(building_task, llm_config)

start_task(
    execution_task="Find a recent paper about gpt-4 on arxiv and find its potential applications in software.",
    agent_list=agent_list,
)