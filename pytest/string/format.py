
# https://docs.python.org/zh-cn/3/library/string.html
# https://docs.python.org/zh-cn/3/library/string.html#formatspec


# replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
# field_name        ::=  arg_name ("." attribute_name | "[" element_index "]")*
# arg_name          ::=  [identifier | digit+]
# attribute_name    ::=  identifier
# element_index     ::=  digit+ | index_string
# index_string      ::=  <any source character except "]"> +
# conversion        ::=  "r" | "s" | "a"
# format_spec       ::=  <described in the next section>

import string

'''
@Description: 主要的API方法。它采用格式字符串和一组任意位置和关键字参数。它只是一个调用vformat（）的包装器。
@Param: 
format_string: 需要去格式化的目标字符串
*args: 任意位置 元组
**kwargs: 关键字参数 字典
@Return: 
'''
# string.Formatter.format(format_string, *args, **kwargs)
data = ("Pi = ",3.1415926)
strtmp = "This is a test:{}{:.4f}"
formatter  = string.Formatter()
strtmp = formatter.format(strtmp,*data) # 元组
print(strtmp)  # This is a test:Pi = 3.1416

data = {"Key1":3.1415926,"Key2":"Pi = "}
strtmp = "This is a test:{Key2}{Key1}"
formatter  = string.Formatter()
strtmp = formatter.format(strtmp,**data)  # 字典
print(strtmp)  # This is a test:Pi = 3.1415926


'''
@Description: 循环遍历format_string并返回一个可迭代的元组（literal_text，field_name，format_spec，conversion）。 vformat（）使用它将字符串分解为文字文本或替换字段。
@Param: 
format_string：需要去格式化的目标字符串
@Return: 
tuples  元组
'''
# string.Formatter.parse(format_string)
strtmp = "This is a test:{}{:.4f}"
formatter  = string.Formatter()
strtuple = formatter.parse(strtmp)

print(strtmp)
for i, v in enumerate(strtuple):
    print(i, v)
    '''
    0 ('This is a test:', '', '', None)
    1 ('', '', '.4f', None)
    '''
strtmp = "This is a test:{Key2}{Key1}"
formatter  = string.Formatter()
strtuple = formatter.parse(strtmp)

print(strtmp)
for i, v in enumerate(strtuple):
    print(i, v)
    '''
    0 ('This is a test:', 'Key2', '', None)
    1 ('', 'Key1', '', None)
    '''
# string.Formatter.parse(format_string) End