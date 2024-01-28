from pywebio.output import *
from pywebio.input import *

def main():
    put_markdown('**AI Master**');

    name = input("What's your name")
    put_markdown("My name is `%s`." % name)

    def on_click(btn):
        put_markdown("You click `%s` button" % btn)
    put_buttons(['Submit'], onclick=on_click);

    # 使用行布局
    put_row([
        put_code('A'), None,
        put_code('B'), None,
        put_code('C')
        ]);

    # 输出进度条
    import time
    put_processbar('bar1');
    for i in range(1, 11):
        set_processbar('bar1', i / 10)  # 更新进度条
        time.sleep(0.1)