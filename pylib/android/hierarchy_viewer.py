
from ppadb.client import Client as AdbClient # # pip install pure-python-adb

import socket


class Activity:
    def __init__(self, line=None):
        self.app_name = None
        self.name = None

        if line is not None:
            self.parser(line)

    def parser(self, line):
        r = line.split()
        if len(r) == 2:
            rr = r[1].split('/')
            self.app_name = rr[0]
            if len(rr) == 2:
                self.name = rr[1]
            else:
                self.name = self.app_name
            self.hashcode = r[0]


class Widget:
    def __init__(self, line=None):
        self.name = None
        self.attrs = {}
        self.level = 0

        self.children = []

        if line is not None:
            self.parser(line)
    
    def parser(self, line):
        org_len = len(line)
        line = line.lstrip()
        self.level = org_len - len(line)

        parts = line.split()
        if len(parts) > 1:
            self.name = parts[0]
            del parts[0]

            for attr in parts:
                attr = attr.split(':')
                if len(attr) == 2:
                    self.attrs[attr[0]] = attr[1]

    def set_parent(self, parent):
        self.parent = parent
        if parent is not None:
            parent._append_child(self)

    def _append_child(self, widget):
        self.children.append(widget)

    def __str__(self):
        ret = []
        # v = 'name: {}, level: {}, attr: {}' % (self.name, self.level, self.attrs)
        v = ' ' * self.level + self.name
        ret.append(v)
        for child in self.children:
            ret.append(str(child))
        return '\n'.join(ret)


class Viewer:
    def  __init__(self, device):
        self.device = device
        self.host = '127.0.0.1'
        self.port = 4939

    def turn_on(self):
        if not self.is_on():
            self.device.shell('service call window 1 i32 ' + str(self.port))
        self.device.forward('tcp:' + str(self.port), 'tcp:' + str(self.port))
        return self.is_on()

    def turn_off(self):
        self.device.shell('service call window 2 i32 ' + str(self.port))

    def is_on(self):
        ret = self.device.shell('service call window 3')
        if ret.find('00000001') > 0:
            return True
        return False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.socket.connect((self.host, self.port))

    def send(self, cmd):
        cmd = bytes(cmd, encoding = "utf8")
        self.socket.send(cmd)

    def recv(self):
        recv = self.socket.recv(10000)
        return str(recv, encoding = "utf-8")

    def recv_to_file(self, fp):
        try:
            while True:
                recv = self.socket.recv(10000)
                fp.write(recv)
        except:
            pass

    def disconnect(self):
        self.socket.close()

    def list_activities(self):
        self.connect()
        self.send('LIST\n')
        recv = self.recv()
        self.disconnect()

        lines = recv.split('\n')
        activities = []
        for line in lines:
            activity = Activity(line)
            if activity.name is not None:
                activities.append(activity)
        return activities

    def dump_widgets(self, activity):
        hashcode = activity.hashcode
        self.connect()
        cmd = ' '.join(('DUMP', hashcode)) + '\n'
        self.send(cmd)
        recv = self.recv()
        self.disconnect()

        top_stack = []

        lines = recv.split('\n')
        line = lines[0]
        del lines[0]
        top_first = Widget(line)
        if top_first.name is not None:
            top_stack.append(top_first)

            for line in lines:
                w = Widget(line)
                if w.name is not None:
                    while True:
                        top = top_stack.pop()
                        if top.level == w.level:
                            top_stack.append(w)
                            break
                        elif top.level < w.level:
                            top_stack.append(top)
                            top_stack.append(w)
                            break
                    w.set_parent(top)
        else:
            top_first = None

        return top_first

    def capture_widget(self, hashcode, widget, filepath=None):
        if filepath is None:
            filepath = widget.name
        self.connect()
        cmd = ' '.join(('CAPTURE', hashcode, widget.name)) + '\n'
        self.send(cmd)
        with open(filepath + '.png', 'wb') as fp:
            self.recv_to_file(fp)
        self.disconnect()


if __name__ == "__main__": # for test
    def error(msg):
        print(msg)
        exit(1)

    def main():
        client = AdbClient()
        devices = client.devices()

        if len(devices) > 0:
            device = devices[0]

            viewer = Viewer(device)
            if not viewer.turn_on():
                error('hierarchy viewer turn on fail!')

            activities = viewer.list_activities()
            for activity in activities:
                print(activity.hashcode, activity.name)

                widget = viewer.dump_widgets(activity)
                if widget is not None:
                    # print(str(widget))
                    filepath = activity.name + '_' + widget.name
                    viewer.capture_widget(activity.hashcode, widget, filepath)
                    print('write file ', filepath)

            viewer.turn_off()


    main()

