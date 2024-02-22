from functools import partial

import datasets

import autogen

endpoint_list = autogen.config_list_openai_aoai()
# the endpoint_list looks like this:
# endpoint_list = [
#     {
#         'api_key': '<your OpenAI API key here>',
#     },  # OpenAI API endpoint for gpt-4
#     {
#         'api_key': '<your first Azure OpenAI API key here>',
#         'base_url': '<your first Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2024-02-15-preview',
#     },  # Azure OpenAI API endpoint for gpt-4
#     {
#         'api_key': '<your second Azure OpenAI API key here>',
#         'base_url': '<your second Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2024-02-15-preview',
#     },  # another Azure OpenAI API endpoint for gpt-4
# ]

config_list = autogen.config_list_from_json(
    env_or_file="config/gen/OAI_CONFIG_LIST",
    filter_dict={
        "model": {
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0301",
            "chatgpt-35-turbo-0301",
            "gpt-35-turbo-v0301",
            "gpt",
        },
    },
)
# the config_list looks like this:
# config_list = [
#     {
#         'model': 'gpt-3.5-turbo',
#         'api_key': '<your OpenAI API key here>',
#     },  # OpenAI API endpoint for gpt-3.5-turbo
#     {
#         'model': 'gpt-3.5-turbo',
#         'api_key': '<your first Azure OpenAI API key here>',
#         'base_url': '<your first Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2024-02-15-preview',
#     },  # Azure OpenAI API endpoint for gpt-3.5-turbo
#     {
#         'model': 'gpt-35-turbo-v0301',
#         'api_key': '<your second Azure OpenAI API key here>',
#         'base_url': '<your second Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2024-02-15-preview',
#     },  # another Azure OpenAI API endpoint for gpt-3.5-turbo with deployment name gpt-35-turbo-v0301
# ]

seed = 41
data = datasets.load_dataset("openai_humaneval")["test"].shuffle(seed=seed)
n_tune_data = 20
tune_data = [
    {
        "definition": data[x]["prompt"],
        "test": data[x]["test"],
        "entry_point": data[x]["entry_point"],
    }
    for x in range(n_tune_data)
]
test_data = [
    {
        "definition": data[x]["prompt"],
        "test": data[x]["test"],
        "entry_point": data[x]["entry_point"],
    }
    for x in range(n_tune_data, len(data))
]