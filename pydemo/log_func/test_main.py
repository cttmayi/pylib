import unittest

from test_case.test_status import *
from test_case.test_parser import *

import os
from sys import argv
os.chdir(os.path.dirname(argv[0]))


if __name__ == '__main__':
    unittest.main()