__author__ = 'agerasym'
from bisect import insort
from collections import deque
from tests.libs import timed_fib
from functools import partial
from time import time
import selectors
import sys
import types


class sleep_for_seconds(object):
    """
    yield the object of this type from a coroutine to have it "sleep" for the
    given number of seconds
    """
    def __init__(self, wait_time):
        self._wait_time = wait_time


class EventLoop(object):
    """
    Implements a simplified coroutine based event loop
    """
    def __init__(self, *tasks):
        self._running = False
        self._selector = selectors.DefaultSelector()

        # Queue of functions scheduled to run
        self._tasks = deque(tasks)

        # (coroutine, stack) pair of tasks waiting for input from stdin
        self._tasks_waiting_on_stdin = []

        # List of (time_to_run, task) paiser, in sorted order
        self._timers = []

        # register for polling stdin for input to read
        self._selector.register(sys.stdin, selectors.EVENT_READ)

    def resume_task(self, coroutine, value=None, stack=()):
        result = coroutine.send(value)
        if isinstance(result, types.GeneratorType):
            self.schedule(result, None, (coroutine, stack))
        elif isinstance(result, sleep_for_seconds):
            self.schedule(result, None, stack, time() + result._wait_time)
        elif result is sys.stdin:
            self._tasks_waiting_on_stdin.append((coroutine, stack))
        elif stack:
            self.schedule(stack[0], result, stack[1])

    def schedule(self, coroutine, value=None, stack=(), when=None):
        """
        Schedule a coroutine task to be run, with value to be sent to it,
        and stack containing the coroutines that are waiting for value yielded
        by this coroutine
        """
        # Bind a parameters to a functino to be scheduled as a function with
        # no parameters.
        task = partial(self.resume_task, coroutine, value, stack)
        if when:
            insort(self._timers, (when, task))
        else:
            self._tasks.append(task)

    def stop(self):
        self._running = False

    def do_on_next_tick(self, func, *args, **kwargs):
        self._tasks.appendleft(partial(func, *args, **kwargs))

    def run_forever(self):
        self._running = True
        while self._running:
            # First check for available IO input
            for key, mask in self._selector.select(0):
                line = key.fileobj.readline().strip()
                for task, stack in self._tasks_waiting_on_stdin:
                    self.schedule(task, line, stack)
                self._tasks_waiting_on_stdin.clear()

            # Next, run the next task
            if self._tasks:
                task = self._tasks.popleft()
                task()

            # Finally run time scheduled tasks
            while self._timers and self._timers[0][0] < time():
                task = self._timers[0][1]
                print('>>>>', type(task), task)
                del self._timers[0]
                task()
        self._running = False


def print_ever(msg, interval):
    """
    Corotine task to repeatedly print the message after the given interval
    (in seconds)
    :param msg:
    :param interval:
    :return:
    """
    while True:
        print("{} - {}".format(int(time()), msg))
        yield sleep_for_seconds(interval)


def read_input(loop: EventLoop):
    """
    Coroutine task for repeatedly read new lines of input from stdin,
    treat the input as a number, calculater and display fib nubmer
    """
    while True:
        line = yield sys.stdin
        if line == 'exit':
            loop.do_on_next_tick(loop.stop)
            continue
        n = int(line)
        print("fib{} is {}".format(n, timed_fib(n)))


def main():
    loop = EventLoop()
    hello_task = print_ever("Hello world", 3)
    fib_task = read_input(loop)
    loop.schedule(hello_task)
    loop.schedule(fib_task)
    loop.run_forever()

if __name__ == '__main__':
    main()





























































