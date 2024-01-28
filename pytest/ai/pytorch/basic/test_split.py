import torch

a = torch.rand(9,4)
print(a)

o = torch.chunk(a, 2, dim=0)
print(o)


o = torch.split(a, 2, dim=0)
print(o)