import pylib.env
import os
import torch
from torch import Tensor
import torch.nn.functional as F
import matplotlib.pyplot as plt
from itertools import chain
from datasets import load_dataset
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
    Qwen2TokenizerFast, Qwen2ForCausalLM
)
from transformers.trainer_utils import get_last_checkpoint

from src.dataset import create_dataset
from src.model import create_model


train_dataset_path = "data/android/1M" # without extension
eval_dataset_path = "data/android/2k" # without extension
test_dataset_path = "data/android/1k" # without extension
model_path = "models/Qwen2.5-0.5B-Instruct"
output_path = "output"

checkpoint = None if not os.path.exists(output_path) else get_last_checkpoint(output_path)

# 训练参数配置
training_args = TrainingArguments(
    output_dir=output_path,
    overwrite_output_dir=True,
    learning_rate=1e-4,
    warmup_ratio=0.1,
    lr_scheduler_type="cosine",
    num_train_epochs=1,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    per_device_eval_batch_size=2,
    eval_strategy="steps",
    save_strategy="steps",
    eval_steps=500,
    save_steps=1_000,  # 保存中间模型
    save_total_limit=10,
    use_cpu=False,
    # bf16=True,
    # save_only_model=True,
    logging_steps=20,
)

device = 'mps' if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'


def forward(model: Qwen2ForCausalLM, data) -> Tensor:
    model.eval()
    input_ids = torch.tensor([data['input_ids']], dtype=torch.long).to(device)
    attention_mask = torch.tensor([data['attention_mask']], dtype=torch.long).to(device)
    with torch.no_grad():
        logits = model(input_ids=input_ids, attention_mask=attention_mask).logits
        logits = F.softmax(logits, dim=-1)
        return logits



if __name__ == '__main__':
    train_dataset =  create_dataset(train_dataset_path)
    eval_dataset = create_dataset(eval_dataset_path)
    model = create_model(model_path)

    # collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    trainer = Trainer(
        model=model,
        args=training_args,
        # data_collator=collator,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )

    trainer.train(resume_from_checkpoint=checkpoint)
    # trainer.save_model()  # 保存模型


    test_dataset = create_dataset(test_dataset_path)
    data = test_dataset[0]


    input_ids = torch.tensor([data['input_ids']], dtype=torch.long).to(device)
    attention_mask = torch.tensor([data['attention_mask']], dtype=torch.long).to(device)

    logits = forward(model, data)

    o_argmax = torch.argmax(logits, dim=-1)
    print('----')
    print(input_ids[:, 1:])
    print(o_argmax)
    o_gather = torch.gather(logits.squeeze(0), 1, input_ids[:, 1:].transpose(0, 1))
    
    print(torch.round(o_gather *100).tolist())

