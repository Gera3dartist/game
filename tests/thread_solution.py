__author__ = 'agerasym'

from threading import Thread
from time import sleep, time
from tests.libs import timed_fib


def print_hello():
    while True:
        print("{} - Hello World".format(int(time())))
        sleep(2)


def read_and_process():
    print('here')
    while True:
        n = int(input())
        print('fib({}) equals: {}'.format(n, timed_fib(n)))


def main():
    print('foo')
    t = Thread(target=print_hello)
    t.daemon = True
    t.start()
    # Main thread will read and process input
    read_and_process()

if __name__ == '__main__':
    main()
