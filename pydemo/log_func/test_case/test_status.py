import unittest
from status import Status, Value, Error

class TestStatus(unittest.TestCase):
    def setUp(self):
        class OBJ(Status):
            def init_attribute(self):
                self.TE = Value(self)
                self.TE_MAP = {}
                self.TE_LIST = []
        status = OBJ()
        self.status = status

    def tearDown(self):
        pass

    def test_class(self):
        status = self.status
        status.set_current_info(10, 1)
        self.assertEqual(status.TE, None)
        self.assertEqual(status.TE.timestamp, 0)

        # 数字
        status.set_current_info(20, 2)
        status.TE = Value(status, 1)
        self.assertEqual(status.TE, 1)
        self.assertLess(status.TE, 2)
        self.assertEqual(status.TE.timestamp, 20)


        status.set_current_info(25, 2)
        status.TE += 2
        self.assertEqual(status.TE, 3)
        self.assertEqual(status.TE.timestamp, 25)

        status.set_current_info(26, 2)
        status.TE -= 3
        self.assertEqual(status.TE,  0)
        self.assertEqual(status.TE.timestamp, 26)

        # 字符串
        status.set_current_info(30, 2)
        status.TE = Value(status, "obj")
        self.assertEqual(status.TE, "obj") 
        self.assertEqual(len(status.TE), 3)
        self.assertEqual(status.TE[0], "o")
        self.assertEqual(status.TE.timestamp, 30)

        status.TE_MAP['ab'] = Value(status, 1)
        status.TE_MAP['cd'] = 2



        status.set_current_info(40, 5)
        status.TE_LIST = [Value(status, 1), Value(status, 2)]
        self.assertEqual(status.TE_LIST[0], 1)
        self.assertEqual(status.TE_LIST[1], 2)
        self.assertEqual(status.TE_LIST[0].timestamp, 40)
        self.assertEqual(status.TE_LIST[1].line, 5)

        # status 状态信息
        v = status.get_all_status()
        # print(v)
        self.assertEqual(v['values']['TE'], "obj")
        self.assertEqual(v['values']['TE_MAP.ab'], 1)
        self.assertEqual(v['values']['TE_MAP.cd'], 2)
        self.assertEqual(v['values']['TE_LIST.0'], 1)
        self.assertEqual(v['values']['TE_LIST.1'], 2)