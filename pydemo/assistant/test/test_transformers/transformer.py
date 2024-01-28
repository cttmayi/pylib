#from transformers.integrations import TensorBoardCallback
#from torch.utils.tensorboard import SummaryWriter
#from transformers import TrainingArguments
#from transformers import Trainer, HfArgumentParser
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
import torch
import torch.nn as nn
#from peft import get_peft_model, LoraConfig, TaskType
from dataclasses import dataclass, field
#import datasets
#import os
from pprint import pprint as print

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)


folder = '/mnt/data/model/'
model_checkpoint = "baichuan-inc/baichuan-7B"

file = folder + model_checkpoint
# tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, trust_remote_code=True)

tokenizer = AutoTokenizer.from_pretrained(file, trust_remote_code=True)

#model = AutoModelForCausalLM.from_pretrained(
#    model_checkpoint, load_in_8bit=False, trust_remote_code=True, 
#    device_map="auto" # 模型不同层会被自动分配到不同GPU上进行计算
#    # device_map={'':torch.cuda.current_device()} # 艹，这个设置有bug，一个小小的baichaun在80G的卡都能爆，换成 auto 立马就好了
#)
model = AutoModelForCausalLM.from_pretrained(file, trust_remote_code=True)

print(model)


def predict(prompts):
    if isinstance(prompts, str):
        prompts = [prompts]
    assert isinstance(prompts, list), 'input should be list of text'

    # # 不加其他参数，不设置 padding，不设置 return pt。这样可以使得每条都保留自己的长度
    input_tensors = tokenizer(prompts, max_length=1024, truncation=True, return_tensors='pt')
    
    #print('input_tensors: ', input_tensors)

    # 再来一次带 padding 的 tokenization
    # tokenizer.padding_side = 'left'
    # input_tensors = tokenizer(prompts, max_length=1024, padding=True, truncation=True, return_tensors='pt')
    prompt_length = input_tensors.input_ids.shape[1]
    input_tensors.to(device)
    

    
    # 下面是 InternLM 专属 generate 参数
    outputs = model.generate(**input_tensors, max_new_tokens=200,   # 按照指定格式，输出差不多就这么长，多了就不用输出了
                            temperature=0.8,
                            top_p=0.8,
                            eos_token_id=(2, 103028),
                            )
    # 过滤掉 prompt 部分
    real_outputs = []
    for i,output in enumerate(outputs):
        # output = output[len(inputs.input_ids[i]):]
        output = output[prompt_length:]
        real_outputs.append(output)
    results = tokenizer.batch_decode(real_outputs, skip_special_tokens=True)

    return results

print(predict('hello.'))