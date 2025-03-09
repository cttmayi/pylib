from status import Status, Value, Error


class DStatus(Status):
    def init_attribute(self):
        self._TE = Value(self)
        self.BUFFER = {}

    def TE(self):
        errors = []

        if self._TE != 1:
            error = Error(self.current_line, 'TE is not 1')
            error.add_related_line(self._TE.line)
            errors.append(error)

        # print(self._TE)
        # print(self._TE.millis)
        # print(self._TE.line)

        self._TE = 1
        return errors
    
    def BQ(self, id):
        print('BQ', id)
        self.BUFFER[id] = Value(self, 1)
        print(self.BUFFER[id].line)


if __name__ == '__main__':
    status = DStatus()
    status.set_current_info(10, 100)
    status.TE()
    print(status.get_all_status())