import numpy as np

n = np.array([[1, 2, 3], [4, 5, 6]])

print(f"{n = }")
print(f"{n.T = }")
print(f"{np.dot(n, n.T) = }")
print(f"{np.eye(3) = }")