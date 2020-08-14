

data = [1,2,3,4,5,6,7,8,9]

def is_odd(n):
    return n % 2 == 1

# 1
ret = list(filter(is_odd, data))
print(ret)

# 2
ret = []
for n in data:
    if is_odd(n):
        ret.append(n)
print(ret)