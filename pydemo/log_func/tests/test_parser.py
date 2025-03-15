import unittest

from lparser.parser import LogParser
from lparser.status import Error

class TestParser(unittest.TestCase):
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


    def verify_error(self, data):
        file = data['file']
        type = data['type']
        errors_verfiy = data['errors']

        errors = self.parser(file, type)
        for msg, line, related_lines in errors_verfiy:
            error = self.get_error(errors, msg)
            self.assertIsNotNone(error)
            self.assertEqual(error.line, line)
            for line in related_lines:
                self.assertIn(line, error.related_lines)

    def test_simple(self):
        data = {
            'file':'test_case/data/simple.log',
            'type': 'debug',
            'errors': [
                ['TE is timeout until end', 32, [30]],
                ['Q is not in BUFFER', 1, [1]],
                ['TE is timeout', 5, [5]],
            ]
        }
        self.verify_error(data)




