

import torch
import numpy as np


def pprint(v:torch.Tensor):
    print('---')
    print(v.type())
    print(v.dtype, v.device, v.layout, v.shape)
    print(v)


v = torch.Tensor([[1,2], [3,4]])
pprint(v)

v = torch.Tensor(2,3)
pprint(v)

v = torch.ones_like(v)
pprint(v)

v = torch.rand(5) # 0~1的随机数
pprint(v)

v = torch.normal(mean=0.0, std=v)
pprint(v)

v = torch.Tensor(2,2).uniform_(-1,1)
pprint(v)

v = torch.arange(0,12,2)
pprint(v)

v = torch.linspace(2,10,4)
pprint(v)

v = torch.randperm(10, dtype=torch.float32)
pprint(v)


#稀疏张量
indices = torch.tensor([[1,2,3], [2,0,2]])
values = torch.tensor([3,4,5])
v = torch.sparse_coo_tensor(indices, values, [2,4])
pprint(v)
v = v.to_dense()
pprint(v)


#指定device
dev = torch.device('mps')
v = torch.tensor([2,2], device=dev)
pprint(v)



