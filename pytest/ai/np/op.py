import numpy as np

n = np.array([[1, 2, 3], [4, 5, 6]])

print(f"{n = }")
print(f"{n.max() = }")
print(f"{n.min() = }")
print(f"{n.argmax(0) = }")
print(f"{n.argmin(0) = }")
print(f"{n.max(0) = }")
print(f"{n.max(1) = }")


print(f"{np.maximum(n, 2) = }")
print(f"{np.minimum(n, 2) = }")

print(f"{np.fmax(n, 2) = }")
print(f"{np.fmin(n, 2) = }")

print(f"{n.ptp() = }") # max - min
print(f"{np.median(n) = }") # 中位数
print(f"{n.sum() = }")
print(f"{n.mean() = }") # 平均
print(f"{n.std() = }") # 标准差
print(f"{n.var() = }") # 方差 = 标准差的平方根


print(f"{n[0] = }")
print(f"{n[0,:] = }")





