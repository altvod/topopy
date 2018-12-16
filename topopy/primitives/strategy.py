from typing import List, Tuple

from topopy.primitives import exc
from .movement import MovementStrategy
from .topology import Topology, Graphable, Location
from .utils import dijkstra


class Strategy:
    """Abstract base class for all strategies"""

    requires_interfaces = ()

    def check_requirements(self, topology: Topology):
        for interface in self.requires_interfaces:
            if not isinstance(topology, interface):
                raise exc.InterfaceError(
                    'Strategy {} requires interface {}'.format(
                       self.__class__.__name__, interface.__name__
                    )
                )


class DistanceStrategy(Strategy):
    """Abstract base class for distance resolution strategies"""

    def get_path(
            self, topology: Topology, actor: MovementStrategy,
            src: Location, dst: Location
    ) -> Tuple[int, List[Location]]:
        raise NotImplementedError


class DijkstraDistanceStrategy(DistanceStrategy):
    requires_interfaces = (
        Graphable,
    )

    def get_path(
            self, topology: Graphable, movement_strategy: MovementStrategy,
            src: Location, dst: Location
    ) -> Tuple[int, List[Location]]:
        graph = topology.to_graph(movement_strategy)
        dist, path = dijkstra.get_shortest_path(graph, src, dst)
        return dist, path
