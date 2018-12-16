from collections import defaultdict
from typing import Generator, List, NamedTuple, Type  #noqa

from .location import Location, Location2D, IntLocation2D
from .movement import MovementStrategy
from .tile import Tile


SQRT_2 = 2.0**0.5


class Topology:
    """Base class for all topologies"""

    __slots__ = ()
    location_class = None  # type: Type[Location]


class Graphable:
    """Interface for topologies convertible to a weighed graph"""

    __slots__ = ()

    def to_graph(self, movement_strategy: MovementStrategy) -> dict:
        raise NotImplementedError


DirectedEdge = NamedTuple('DirectedEdge', (
    ('from_loc', Location),
    ('to_loc', Location),
    ('from_tile', Tile),
    ('to_tile', Tile),
))


class GraphableTopology(Topology, Graphable):
    """Topology that can be converted to a weighted graph."""

    __slots__ = ()

    def get_edges(self, loc: Location) -> List[DirectedEdge]:
        raise NotImplementedError

    def all_locations(self) -> Generator[Location, None, None]:
        raise NotImplementedError

    def __getitem__(self, loc: Location):
        raise NotImplementedError

    def __setitem__(self, loc: Location, value: Tile):
        raise NotImplementedError

    def to_graph(self, movement_strategy: MovementStrategy) -> dict:
        graph = defaultdict(dict)
        for loc in self.all_locations():
            for from_loc, to_loc, from_tile, to_tile in self.get_edges(loc):
                p = movement_strategy.get_passability(
                    from_loc=from_loc, to_loc=to_loc,
                    from_tile=from_tile, to_tile=to_tile
                )
                if p is not None:
                    graph[from_loc][to_loc] = p

        return dict(graph)


class RectangularTopology(GraphableTopology):
    """Rectangular matrix-based topology with 2D coordinates."""

    __slots__ = 'matrix', 'tile_class'
    location_class = IntLocation2D

    def __init__(self, matrix: List[List[Tile]]):
        if not matrix:
            raise ValueError('Matrix cannot be empty')
        row_len = len(matrix[0])
        for row in matrix:
            if len(row) != row_len:
                raise ValueError('Matrix rows must be of the same length')

        self.matrix = matrix

    def __getitem__(self, loc: Location2D):
        if not isinstance(loc, self.location_class):
            raise TypeError(loc.__class__.__name__)

        return self.matrix[loc.x][loc.y]

    def __setitem__(self, loc: Location2D, value: Tile):
        if not isinstance(loc, self.location_class):
            raise TypeError(loc.__class__.__name__)

        self.matrix[loc.x][loc.y] = value

    def get_edges(self, loc: Location2D) -> List[DirectedEdge]:
        x_limit = len(self.matrix)
        y_limit = len(self.matrix[0])
        edges = []
        for x1 in range(max(0, loc.x - 1), min(x_limit, loc.x + 2)):
            for y1 in range(max(0, loc.y - 1), min(y_limit, loc.y + 2)):
                if x1 == loc.x and y1 == loc.y:
                    continue
                to_loc = self.location_class(x1, y1)
                edges.append(
                    DirectedEdge(loc, to_loc, self[loc], self[to_loc])
                )

        return edges

    def all_locations(self) -> Generator[Location2D, None, None]:
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                yield self.location_class(x, y)


#   *---*---*---*---*---*
#  / \ / \ / \ / \ / \ /
# *---*---*---*---*---*
#  \ / \ / \ / \ / \ / \
#   *---*---*---*---*---*
#  / \ / \ / \ / \ / \ /
# *---*---*---*---*---*
#  \ / \ / \ / \ / \ / \
#   *---*---*---*---*---*
#  / \ / \ / \ / \ / \ /
# *---*---*---*---*---*
#  \ / \ / \ / \ / \ / \
#   *---*---*---*---*---*
#
#
#   *---*       *---*
#  /     \     /     \
# *       *---*       *--
#  \     /     \     /
#   *---*       *---*
#  /     \     /     \
# *       *---*       *--
#  \     /     \     /
#   *---*       *---*
#  /     \     /     \
# *       *---*       *--
#  \     /     \     /
#   *---*       *---*
