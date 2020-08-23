


# pip install imageio

from ppadb.client import Client as AdbClient

import socket
# import imageio
# import io

import sys
import time

class Viewer:
    def  __init__(self, device):
        self.device = device
        self.host = '127.0.0.1'
        self.port = 4939

    def turn_on(self):
        if not self.is_on():
            self.device.shell('service call window 1 i32 4939')
        self.device.forward('tcp:4939', 'tcp:4939')
        return self.is_on()

    def turn_off(self):
        self.device.shell('service call window 2 i32 4939')

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
        ret = {}
        for line in lines:
            r = line.split()
            if len(r) == 2:
                ret[r[1]] = r[0]
        return ret

    def dump_activity(self, hashcode):
        self.connect()
        cmd = ' '.join(('DUMP', hashcode)) + '\n'
        self.send(cmd)
        recv = self.recv()
        self.disconnect()

        lines = recv.split('\n')
        ret = []
        for line in lines:
            if line[0] != ' ':
                r = line.split()
                if len(r) > 0:
                    ret.append(r[0])
        return ret

    def dump_widget(self, hashcode, widget, filepath=None):
        if filepath is None:
            filepath = widget
        self.connect()
        cmd = ' '.join(('CAPTURE', hashcode, widget)) + '\n'
        self.send(cmd)
        with open(filepath + '.png', 'wb') as fp:
            self.recv_to_file(fp)
        self.disconnect()


if __name__ == "__main__": # for test
    def error(msg):
        print(msg)
        exit(1)

    def main(app_name):
        client = AdbClient()
        devices = client.devices()

        if len(devices) > 0:
            device = devices[0]

            viewer = Viewer(device)
            if not viewer.turn_on():
                error('hierarchy viewer turn on fail!')

            activities = viewer.list_activities()
            for activity in activities:
                hashcode = activities[activity]
                if activity.find(app_name) > 0:
                    activity = activity.split('/')[1]
                    print(hashcode, activity)
                    widgets = viewer.dump_activity(hashcode)
                    for widget in widgets:

                        filepath = activity + '_' + widget
                        viewer.dump_widget(hashcode, widget, filepath)
                        print('write file ', filepath)

            viewer.turn_off()


    main('Setting')

