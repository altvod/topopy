from collections import namedtuple
from functools import wraps
from typing import Callable


class Location:
    __slots__ = ()


def _comparison(method: Callable):
    @wraps(method)
    def wrapper(self, other):
        if isinstance(other, self.__class__):
            return method(self, other)
        else:
            return getattr(super(), method.__name__)(other)

    return wrapper


_Location2D = namedtuple('_Location2D', ('x', 'y'))


class Location2D(_Location2D, Location):
    __slots__ = ()


class IntLocation2D(Location2D):
    """2D-location with integer coordinates"""
    __slots__ = ()
