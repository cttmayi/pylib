import torch
import torch.nn as nn
import numpy as np

class CustomTransformer(nn.Module):
    def __init__(self, vocab_size, embedding_dim, d_model, num_heads, num_layers):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.linear = nn.Linear(embedding_dim + 2, d_model)
        self.transformer = nn.Transformer(d_model=d_model, nhead=num_heads, num_encoder_layers=num_layers)

    def forward(self, x):
        string_embeddings = self.embedding(x[:, :, 0].long())
        combined_embeddings = torch.cat((string_embeddings, x[:, :, 1:]), dim=-1)
        input_embeddings = self.linear(combined_embeddings)
        src = input_embeddings.permute(1, 0, 2)  # 调整维度为 (seq_length, batch_size, d_model)
        tgt = src.clone()  # 目标序列与源序列相同
        output = self.transformer(src, tgt)
        return output

# 数据
data = [("apple", 2, 3), ("banana", 4, 5), ("apple", 6, 7)]
vocab = {"apple": 0, "banana": 1, "orange": 2}

# 编码字符串
encoded_data = [(vocab[item[0]], item[1], item[2]) for item in data]
values = np.array([item[1:] for item in encoded_data])
normalized_values = (values - values.mean(axis=0)) / values.std(axis=0)
normalized_data = [(encoded[0], normalized_values[i][0], normalized_values[i][1]) for i, encoded in enumerate(encoded_data)]

# 转换为张量
input_tensor = torch.tensor(normalized_data, dtype=torch.float32).unsqueeze(0)  # 添加 batch 维度

# 模型
model = CustomTransformer(vocab_size=len(vocab), embedding_dim=16, d_model=32, num_heads=4, num_layers=2)
output = model(input_tensor)
print(output)