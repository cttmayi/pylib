import torch

tensor_0 = torch.arange(1, 10).view(3, 3)
print(tensor_0)


index = torch.tensor([[2, 1, 0]])
tensor_1 = tensor_0.gather(0, index)
print(tensor_1)


index = torch.tensor([[2, 1, 0]])
tensor_1 = tensor_0.gather(1, index)
print(tensor_1)


index = torch.tensor([[2, 1, 0]]).t()
tensor_1 = tensor_0.gather(1, index)
print(tensor_1)

index = torch.tensor([[0, 2], 
                      [1, 2]])
tensor_1 = tensor_0.gather(1, index)
print(tensor_1)