import torch


a = torch.rand(5)
b = torch.rand(5)

print(a)
print(b)
print(torch.eq(a,b))
print(torch.equal(a,b))
print(torch.ge(a,b))
print(torch.gt(a,b))
print(torch.le(a,b))
print(torch.lt(a,b))
print(torch.ne(a,b))

print(torch.sort(a))