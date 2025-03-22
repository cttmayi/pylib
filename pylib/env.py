import os
from sys import argv
import dotenv


# load golbal environment variables 
if os.path.exists('.env'):
    dotenv.load_dotenv('.env', override=True)
    print('load global env file')

# enter the directory of the project
path = argv[0]
if path is not None and path != '':
    os.chdir(os.path.dirname(argv[0]))
    print('enter project directory')

# load project environment variables
if os.path.exists('.env'):
    dotenv.load_dotenv('.env', override=True)
    print('load project env file')