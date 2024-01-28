import torch

a = torch.zeros((2,4))

b = torch.ones((2,4))


print(a)

print(b)

c = torch.cat((a, b), dim=0)
print(c)

c = torch.cat((a, b), dim=1)
print(c)