import os
from sys import argv

path = argv[0]
if path is not None and path != '':
    os.chdir(os.path.dirname(argv[0]))
