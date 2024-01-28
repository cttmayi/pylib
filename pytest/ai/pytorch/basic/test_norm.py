import torch




a = torch.rand(1,1)
b = torch.rand(1,1)


print(a)
print(b)

c = torch.norm(a)
print(c)

c = torch.dist(a,b, 2)
print(c)