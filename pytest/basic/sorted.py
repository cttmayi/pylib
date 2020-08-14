

data = [1, 7, 4, 3, 9, -4, -2]

ret = sorted(data)
print(ret)

# 对abs(1), abs(7), 进行比较
ret = sorted(data, key=abs)
print(ret)

# 取反方向排序
ret = sorted(data, reverse=True)
print(ret)