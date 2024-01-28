
r1 = 3

code = 'result = r1 + 2'
local_vars = {}
exec(code, globals(), local_vars)
result = local_vars['result']
print(result)