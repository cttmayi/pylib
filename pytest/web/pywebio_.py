from pywebio.input import input
from pywebio.output import put_text

def drag_control_demo():
    value = input("Drag to adjust value", validate=lambda x: 0 <= x <= 100)
    put_text('Current value: %d' % value)

if __name__ == '__main__':
    drag_control_demo()


