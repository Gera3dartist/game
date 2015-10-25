__author__ = 'agerasym'
import asyncio

def coroutine():
    print('Starting')
    try:
        yield "Let's pause until continued."
        print('Continuing')
    except Exception as e:
        yield "Got an exception: " + str(e)


def main1():
    c = coroutine()
    next(c)
    value = c.throw(Exception("have an exceptional day!"))
    print(value)


@asyncio.coroutine
def A():
    raise Exception("Something went wrong in A!")


@asyncio.coroutine
def B():
    a = yield from A()
    yield a + 1

@asyncio.coroutine
def C():
    try:
        b = yield from B()
        print(b)
    except Exception as e:
        print("C got exception: ", e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(C())

if __name__ == '__main__':
    main()
