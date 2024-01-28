


'''
广播机制: 张量参数可以自动扩展为相同大小。 可简化操作
满足2个条件
1. 每个张量至少有一个维度
2. 满足右对齐， 最后一个维度相等或者为1

'''


import torch

a = torch.ones(2,2)
b = torch.ones(1,2)

c = a + b
print(c)

a = torch.ones(2,1)
b = torch.ones(1,2)

c = a + b
print(c)