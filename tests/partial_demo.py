__author__ = 'agerasym'

from functools import partial


class Power(type):
    def __init__(cls, name, bases, dct):
        for el in range(10):
            setattr(cls, "power{}".format(el),
                    partial(cls.power, exponent=el))
        super(Power, cls).__init__(name, bases, dct)

    def power(cls, base, exponent):
        return base ** exponent


class CustomPower(metaclass=Power):
    pass


if __name__ == '__main__':
    p = CustomPower()
    print(p.power3(2))


