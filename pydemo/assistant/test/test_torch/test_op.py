

import torch

a = torch.Tensor([[1,2], [3,4]])
b = torch.Tensor([[1,2], [3,4]])

c = a + b
print(c)

c = torch.add(a,b)
print(c)

c = a.add(b)
print(c)

a.add_(b)
print(a)

a = torch.Tensor([[1,2], [3,4]])
b = torch.Tensor([[1,2], [3,4]])

c = a - b #
print(c)
c = a * b #mul
print(c)
c = a / b #div
print(c)
c = a.sqrt()
print(c)
c = a.exp()
print(c)

# 矩阵运算

a = torch.Tensor([[1,2], [3,4]])
b = torch.Tensor([[1,2], [3,4]])

c = a @ b
print(c)

c = torch.mm(a, b) # 二维
print(c)

a = torch.ones(2,3,2)
b = torch.ones(2,2,3)

c = torch.matmul(a, b) # 高维
print(c)