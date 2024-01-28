import torch

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")



N_FEATURE = 13
N_OUTPUT = 1
T_TRAIN = 10000

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, 1000)
        self.predict = torch.nn.Linear(1000, n_output)
        pass

    def forward(self, x):
        out = self.hidden(x)
        out = torch.relu(out)
        out = self.predict(out)
        return out
    
net = Net(N_FEATURE, N_OUTPUT)


loss_func = torch.nn.MSELoss()


optimizer = torch.optim.SGD(net.parameters(), lr=0.01)


X = torch.rand(1000, N_FEATURE)
Y = torch.rand(1000, N_OUTPUT)


for i in range(T_TRAIN):
    pred = net.forward(X)
    # pred = torch.squeeze(pred)
    loss = loss_func(pred, Y)
    # print(Y.shape, pred.shape)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print('ite:{}, loss:{}'.format(i, loss))
    print(pred[0], Y[0])
