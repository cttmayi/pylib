from pywebio.output import *

def main():
    # 输出文本
    put_text("Hello world!");

    # 输出表格
    put_table([
        ['Product', 'Price'],
        ['Apple', '$5.5'],
        ['Banner', '$7'],
    ]);

    # 输出图像
    # put_image(open('python-logo.png', 'rb').read());

    # 输出MarkDown
    put_markdown('**Bold text**');

    # 输出通知消息
    toast('Awesome PyWebIO!!');

    # 输出文件
    put_file('hello_word.txt', b'hello word!');

    # 输出Html
    put_html('E = mc<sup>2</sup>');

    # 显示弹窗
    with popup('Popup title'):
        put_text("Hello world!")
        put_table([
            ['Product', 'Price'],
            ['Apple', '$5.5'],
            ['Banner', '$7'],
        ])


    # 输出可以点击的按钮
    def on_click(btn):
        put_markdown("You click `%s` button" % btn)

    put_buttons(['A', 'B', 'C'], onclick=on_click);


    # 使用行布局
    put_row([put_code('A'), None, put_code('B')]);

    # 输出进度条
    import time
    put_processbar('bar1');
    for i in range(1, 11):
        set_processbar('bar1', i / 10)  # 更新进度条
        time.sleep(0.1)
