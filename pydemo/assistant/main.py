
from utils.spinner import Spinner

def main():

    with Spinner('Thinking ...'):
        import time
        time.sleep(10)
    print('Think Done')


if __name__ == '__main__':
    main()
