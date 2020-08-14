

data = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 1
ret = []
for n in data:
    ret.append(f(n))
print(ret)

# 2
def f(x):
    return x * x

ret = list(map(f, data))
print(ret)

######################################################

