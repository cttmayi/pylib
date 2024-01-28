from huggingface_hub import hf_hub_download

hf_hub_download(repo_id="baichuan-inc/baichuan-7B", filename="config.json", cache_dir="./test/model/baichuan")