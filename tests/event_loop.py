__author__ = 'agerasym'

import selectors
import sys
from time import time
from tests.libs import timed_fib


def process_input(stream):
    text = stream.readline()
    n = int(text.strip())
    print('fib({}) = {}'.format(n, timed_fib(n)))


def print_hello():
    print("{} - Hello worlds".format(int(time())))


def main():
    selector = selectors.DefaultSelector()
    # Register selector to poll for input from stdin
    selector.register(sys.stdin, selectors.EVENT_READ)
    last_hello = 0
    while True:
        # Wait at most 100 miliseconds for input to be available
        for event, mask in selector.select(0.1):
            process_input(event.fileobj)
        if time() - last_hello > 3:
            last_hello = time()
            print_hello()

if __name__ == '__main__':
    main()
