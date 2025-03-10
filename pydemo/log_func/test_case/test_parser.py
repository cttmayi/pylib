import unittest

from parser import LogParser
from status import Error

class TestStatus(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def parser(self, file, type):
        lp:LogParser = LogParser(file, type)
        logs = lp.transfor_to_df()
        ops = lp.transfor_to_op(logs)

        errors = lp.op_execute(ops)

        return errors

    def get_error(self, errors, msg, level = None) -> Error:
        for error in errors:
            # print(error.msg, error.msg == msg, level is None or error.level == level)
            if (level is None or error.level == level) and error.msg == msg:
                return error
        return None

    def test_simple(self):
        file = 'log/test/simple.log'
        type = 'debug'
        errors = self.parser(file, type)

        error = self.get_error(errors, 'TE is timeout until end')
        self.assertIsNotNone(error)
        self.assertIn(30, error.related_lines)

    def test_file_group(self):
        file_data = [
            ['log/test/simple.log' , 'debug', 'TE is timeout until end', 32, [30]]
        ]

        for file, type, msg, line, related_lines in file_data:
            errors = self.parser(file, type)
            error = self.get_error(errors, msg)
            self.assertIsNotNone(error)
            self.assertEqual(error.line, line)
            for line in related_lines:
                self.assertIn(line, error.related_lines)



