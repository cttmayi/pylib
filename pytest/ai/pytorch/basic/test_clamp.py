import torch


a = torch.rand(2)


print(a)

a = torch.clamp(a, 0, 0.5)
# a = a.clamp(0, 0.5)


print(a)
