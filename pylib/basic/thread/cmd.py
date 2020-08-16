
import os
import signal
import subprocess
import threading
import wx
import tempfile
import time
import thread


def run_cmd(cmd, timeout = 0, callback = None):
    out = ''
    thread = CmdThread(cmd)
    thread.start()
    wait_remaining_sec = timeout
    proc = thread.get_popen()
    while proc.poll() is None and (timeout == 0 or wait_remaining_sec > 0):
        time.sleep(0.5)
        wait_remaining_sec -= 0.5
        print(wait_remaining_sec)
        data = thread.read_line()
        while(data != None):
            print('cbk')
            out = out + data
            if callback != None:
                callback(data)
                print(data)
            data = thread.read_line()
        #print wait_remaining_sec
    if wait_remaining_sec <= 0 and timeout != 0:
        stop_cmd_by_PID(proc.pid)
    return out


def stop_cmd_by_PID(pid):
    os.kill(pid, signal.SIGINT)


class CmdThread(threading.Thread):
	def __init__(self, cmd):
		threading.Thread.__init__(self)
		self.data = []
		self.cmd = cmd
		self.popen = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
		self.output_pipe =  self.popen.stdout
		self.mutex = threading.Lock()


	def get_popen(self):
		return self.popen


	def read_line(self):
		self.mutex.acquire()
		if len(self.data) > 0:
			ret = self.data[0]
			del self.data[0]
		else:
			ret = None
		self.mutex.release()
		return ret


	def run(self):
		while (True):
			string =  self.output_pipe.readline()
			if (string):
				self.mutex.acquire()
				self.data.append(string)
				self.mutex.release()
			else:
				break
