from status import Status, Value, Error
from utils.timestamp import s, ms, us


class DStatus(Status):
    def init_attribute(self):
        self.te = Value(self, 0)
        self.buffer = {}

    def end_checker(self):
        with Error(self, 'TE is timeout until end', Error.CRITICAL) as error:
            if self.DURATION(self.te) > ms(150) and self.mode is not None:
                self.raise_error(error)

    def TE(self):
        with Error(self, 'TE is timeout', Error.WARNING) as error:
            if self.DURATION(self.te) > ms(150) and self.mode is not None:
                self.raise_error()

        self.te = Value(self, 1)

    def DQ(self, id):
        self.buffer[id] = Value(self, 1)

    def Q(self, id):

        with Error(self, 'Q is not in BUFFER', Error.ERROR) as error:
            if id not in self.buffer and self.TIMESTAMP > ms(100):
                self.raise_error()
        with Error(self, 'Q is timeout', Error.WARNING) as error:
            if self.DURATION(self.buffer.get(id)) > ms(100) and self.mode > 60: # mode is defined in g.py
                # error.add_related_line(self.BUFFER[id].LINE) # 需要手动添加输出的行数
                self.raise_error()

        if id in self.buffer:
            del self.buffer[id]

STATUS = DStatus()

if __name__ == '__main__':
    STATUS.set_current_info(10, 100)
    STATUS.TE()
    STATUS.DQ(1)
    print(STATUS.get_all_status())