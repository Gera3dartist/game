from functools import wraps

__author__ = 'agerasym'
import time


def fib(n):
    return fib(n-1) + fib(n-2) if n > 1 else n


def gen_fib(n):
    if n < 1:
        yield n
    else:
        a = yield gen_fib(n-1)
        b = yield gen_fib(n-2)
        yield a + b


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time() - start
        print('function took: ', end)
        return result
    return wrapper

timed_fib = timed(fib)

