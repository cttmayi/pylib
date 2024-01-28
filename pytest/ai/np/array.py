import numpy as np

print('arrsy: ', np.array([1, 2, 3, 4, 5]))
print('ones: ', np.ones(12))
print('empty: ', np.empty(12))
print('full: ', np.full(12, 7))
print('linspace: ', np.linspace(0, 1, 6))
print('logspace: ', np.logspace(0, 9, 6, base=10))
print('random: ', np.random.rand(12))
print('random int: ', np.random.randint(10, size=(4, 4)))
print('zeros: ', np.zeros(12))
print('identity: ', np.eye(4))
print('identity: ', np.identity(4))
print('diag: ', np.diag([2, 3, 4]))
print('diag: ', np.diag([2, 3, 4], k=1))
print('diag: ', np.diag([2, 3, 4], k=-1))
print('diag: ', np.diag([[1, 2], [3, 4]]))
print('diag: ', np.diag([[1, 2], [3, 4]], k=1))
print('diag: ', np.diag([[1, 2], [3, 4]], k=-1))
print('arrange', np.arange(12))
print('arrange', np.arange(12, 24))
print('arrange', np.arange(12, 24, 2))


n = np.array([1, 2, 3, 4, 5])

print('n.shape: ', n.shape)

print('n.ndim', n.ndim)
print('n.size', n.size)
print('n.dtype', n.dtype)
print('n.itemsize', n.itemsize)
print('n.data', n.data)
print('n.T', n.T)
print('n.transpose', n.transpose())
print('n.flatten', n.flatten())
print('n.ravel', n.ravel())



n = np.array([[1, 2, 3, 4, 5], [11,12,13,14,15]])

print('n[: ,0:2]\n', n[: ,0:2])
print('n[0, 0]', n[0, 0])
print('n[0, :]', n[0, :])
print('n[0, 2]', n[0, 2])
print('n[0, -1]\n', n[0, -1])
print('n[:, ::-1]\n', n[:, ::-1]) # 翻转


#reshape
n = np.array([1, 2, 3, 4, 5, 6])
print('n.reshape: \n', n.reshape(6, 1))
print('n.reshape: \n', n.reshape(1, 6))
print('n.reshape(-1, 1)\n', n.reshape(-1, 2))
print('n.reshape(5, -1)\n', n.reshape(3, -1))


n = np.array([[1, 2, 3], [4, 5, 6]])
n2 = np.array([[1, 2, 3], [4, 5, 6]])

print('n + n2: \n', n + n2)
print('n - n2: \n', n - n2)

print(np.concatenate([n, n2]))
print(np.concatenate([n, n2], axis=0))
print(np.concatenate([n, n2], axis=1))






