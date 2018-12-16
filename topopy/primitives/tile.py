from functools import lru_cache
from typing import Any


class Tile:
    """
    The base element that makes up simple topologies
    """

    __slots__ = ()


class KeyTile(Tile):
    """
    A ``Tile`` that is defined by a single value, its *key*
    """

    __slots__ = 'key',

    @classmethod
    @lru_cache(None)
    def from_key(cls, key: Any):
        return KeyTile(key)

    def __init__(self, key: Any):
        self.key = key

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.key == other.key
        else:
            return super().__eq__(other)

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.key)

    def __str__(self):
        return str(self.key)
