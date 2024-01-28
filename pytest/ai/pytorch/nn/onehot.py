import torch
import torch.nn.functional as F

x = torch.arange(2,5)

F.one_hot(x)

print(F.one_hot(x))

print(F.one_hot(x, num_classes=10))



import numpy as np
samples = ['the cat sat on the mat.','the dog ate my homework','the chicken is delicious']
token_index = {}  # 单词和索引组成的字典
for sample in samples:
    for word in sample.split():  # 利用 split 方法对样本进行分词。在实际应用中，还需要从样本中去掉标点和特殊字符
        if word not in token_index:
            token_index[word] = len(token_index)+1  # 为每个唯一单词指定一个唯一索引。注意，没有为索引编号 0 指定单词

max_length = 10  # 对样本进行分词。只考虑每个样本前 max_length 个单词。这里的样本指的是samples里的每个元素，比如'the cat sat on the mat.'
results = np.zeros(shape=(len(samples),max_length,max(token_index.values())+1))
for i,sample in enumerate(samples):
    for j,word in list(enumerate(sample.split()))[:max_length]:
        index = token_index.get(word)
        results[i,j,index] =1
        # i表示样本的索引，比如results[0]表示第一个样本，results[1]表示第二个样本，i+1就表示总共的样本数
        # 从results的定义来看，这里用了[max_length,max(token_index.values())+1]维的矩阵来表示一个样本

# 下面几个打印是对上面一些东西的说明
print("token_index:\n",token_index)
print("token_index.values():\n",token_index.values())
print("list(enumerate('the cat sat on the mat.'.split())):\n",list(enumerate('the cat sat on the mat.'.split())))
print("results[0]:\n",results[0])  # results[0]矩阵就是'the cat sat on the mat.'的onehot表示
print(F.one_hot(torch.tensor(token_index)))
