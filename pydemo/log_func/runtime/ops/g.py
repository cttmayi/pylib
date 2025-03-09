from status import Status, Value, Error


class GStatus(Status):
    def init_attribute(self):
        self.mode = None

    def MODE_INIT(self, last, mode):
        if self.mode is None:
            self.mode = Value(self, last)

    def MODE(self, last, mode):
        self.mode = Value(self, mode)

        with Error(self, 'Mode change', Error.INFO) as error:
            if self.mode is not None:
                self.raise_error()

STATUS = GStatus()