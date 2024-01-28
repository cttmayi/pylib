# 新的格式化字符串方式
# 新的格式化字符串方式，即在普通字符串前添加 f 或 F 前缀，其效果类似于str.format()。比如
name = "red"
print(f"He said his name is {name}.") # 'He said his name is red.'
print("He said his name is {name}.".format(**locals())) # 'He said his name is red.'


# 此外，此特性还支持嵌套字段，比如：
width = 10
precision = 4
value = "12.34567"
print(f"result: {value:{width}.{precision}}") # 12.3


# 通过 : 后跟 浮点数标识 ，可以实现格式化浮点数
val = 11
print(f'{val:.3f}')  # 11.000
print(f'{val:.4f}')  # 11.0000


# 格式化宽度
for i in range(1, 4):
    print(f'{i:02} {i * i:3} {i * i * i:4}')
# 01   1    1
# 02   4    8
# 03   9   27
# 04  16   64


# 对齐字符串
s1 = 'a'
s2 = 'ab'
# 将输出的宽度设置为十个字符。 使用 > 符号，让输出结果右对齐。
print(f'{s1:>10}')
print(f'{s2:>10}')
#          a
#         ab
# 实际上，只要大于最大的字符串长度，就可以实现右对齐，感兴趣可以试下小于最大字符串长度会有什么表现


print(f"{s1 = }") # s1 = 'a'



