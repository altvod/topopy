from typing import Any, Callable, List, Type

from topopy.primitives.topology import Topology, RectangularTopology
from topopy.primitives.tile import KeyTile


class TopologySerializer:
    """Allows the conversion of data <--> topology conversion"""

    topology_class = None  # type: Type[Topology]

    def deserialize(self, data: Any) -> Topology:
        raise NotImplementedError

    def serialize(self, topology: Topology) -> Any:
        raise NotImplementedError


class RectangularSerializerBase(TopologySerializer):
    topology_class = RectangularTopology
    tile_factory = KeyTile.from_key

    def __init__(self, topology_class: Type[RectangularTopology]=None,
                 tile_factory: Callable=None):
        self.topology_class = topology_class or self.topology_class
        self.tile_factory = tile_factory or self.tile_factory


class RectangularCharSerializer(RectangularSerializerBase):
    def __init__(self, *args, sep='\n', **kwargs):
        super().__init__(*args, **kwargs)
        self.sep = sep

    def deserialize(self, data: str) -> 'RectangularTopology':
        matrix = [
            [self.tile_factory(char) for char in line.strip(self.sep)]
            for line in data.strip(self.sep).split(self.sep)
        ]
        return self.topology_class(matrix)

    def serialize(self, topology: RectangularTopology) -> str:
        return self.sep.join([
            ''.join([str(tile) for tile in row])
            for row in topology.matrix
        ])


class RectangularKeySerializer(RectangularSerializerBase):
    def deserialize(self, matrix: List[List[Any]]) -> 'RectangularTopology':
        matrix = [
            [self.tile_factory(key) for key in row]
            for row in matrix
        ]
        return self.topology_class(matrix)

    def serialize(self, topology: RectangularTopology) -> list:
        return [
            [tile.key for tile in row]
            for row in topology.matrix
        ]
