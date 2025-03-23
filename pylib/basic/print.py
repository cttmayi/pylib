from colorama import Fore, Style, init
init()

def print_truncated(*args, **kwargs):
    placeholder=kwargs.pop('placeholder', '...')
    separator=kwargs.pop('separator', '\n')
    truncated_line_number = kwargs.pop('truncated_line_number', 7)
    text = ' '.join(args)

    before_line_num = truncated_line_number // 2
    after_line_num = truncated_line_number - before_line_num - 1

    lines = text.strip().split(separator)
    truncated_lines = []
    is_truncated = True
    for line_number, line in enumerate(lines):
        if line_number < before_line_num or line_number >= len(lines) - after_line_num:
            truncated_lines.append(line)
        else:
            if is_truncated:
                truncated_lines.append(placeholder)
                is_truncated = False
    print(separator.join(truncated_lines))

def _print_colored(*args, **kwargs):
    color = kwargs.pop('color', None)
    truncated_line_number = kwargs.pop('truncated_line_number', None)
    if color:
        print(color, end='')  # 设置为红色
    if truncated_line_number:
        print_truncated(*args, **kwargs, truncated_line_number=truncated_line_number)
    else:
        print(*args, **kwargs)  # 打印传入的参数
    if color:
        print(Fore.RESET, end='')  # 重置颜色

def print_normal(*args, **kwargs):
    _print_colored(*args, **kwargs)

def print_red(*args, **kwargs):
    _print_colored(*args, color=Fore.RED, **kwargs)

def print_green(*args, **kwargs):
    _print_colored(*args, color=Fore.GREEN, **kwargs)

def print_yellow(*args, **kwargs):
    _print_colored(*args, color=Fore.YELLOW, **kwargs)

def print_blue(*args, **kwargs):
    _print_colored(*args, color=Fore.BLUE, **kwargs)

def print_info(*args, **kwargs):
    _print_colored(*args, color=Fore.CYAN, **kwargs)

def print_warning(*args, **kwargs):
    _print_colored(*args, color=Fore.YELLOW, **kwargs)

def print_error(*args, **kwargs):
    _print_colored(*args, color=Fore.RED, **kwargs)


if __name__ == '__main__':
    print_red('Role:', )
    # 示例用法
    input = '''这是一个非常非常非常长的字符串，
    需要被截断。
    这是一个非常非常非常长的字符串，
    需要被截断。
    这是一个非常非常非常长的字符串，
    需要被截断。
    这是一个非常非常非常长的字符串，
    需要被截断。
    这是一个非常非常非常长的字符串，
    需要被截断。
    这是一个非常非常非常长的字符串，
    需要被截断。
    这是一个非常非常非常长的字符串，
    需要被截断。
    这是一个非常非常非常长的字符串，
    需要被截断。
    这是一个非常非常非常长的字符串
    '''
    print_normal(input, truncated_line_number=5)