from unittest import TestCase

from topopy.primitives.strategy import DijkstraDistanceStrategy
from topopy.primitives.tile import KeyTile

from topopy.primitives.movement import (
    MovementStrategy, SimpleRectangularMovement
)
from topopy.serialization.topology import RectangularCharSerializer


class TestDijkstraDistanceStrategy(TestCase):
    def _check_path(
            self, topo_str: str, expected_str: str,
            movement_strategy: MovementStrategy,
            start: tuple, end: tuple
    ):
        t = KeyTile.from_key
        topo = RectangularCharSerializer().deserialize(topo_str)
        strategy = DijkstraDistanceStrategy()
        dist, path = strategy.get_path(
            topology=topo,
            movement_strategy=movement_strategy,
            src=topo.location_class(*start),
            dst=topo.location_class(*end),
        )

        for loc in path:
            topo[loc] = t('o')
        self.assertEqual(
            expected_str.strip(),
            RectangularCharSerializer().serialize(topo).strip()
        )

    def test_get_shortest_path_no_diag(self):
        topo_str = (
            '..#..\n'
            '.##..\n'
            '.....\n'
            '.##..\n'
        )
        movement_strategy = SimpleRectangularMovement(
            diagonal=False,
            weight_map={('.', '.'): 1}
        )
        expected_str = (
            'o.#..\n'
            'o##..\n'
            'oooo.\n'
            '.##o.\n'
        )
        self._check_path(topo_str, expected_str, movement_strategy,
                         (0, 0), (3, 3))

    def test_get_shortest_path_diag(self):
        topo_str = (
            '..#..\n'
            '.##..\n'
            '.....\n'
            '.##..\n'
        )
        movement_strategy = SimpleRectangularMovement(
            diagonal=True,
            weight_map={('.', '.'): 1}
        )
        expected_str = (
            'o.#..\n'
            'o##..\n'
            '.oo..\n'
            '.##o.\n'
        )
        self._check_path(topo_str, expected_str, movement_strategy,
                         (0, 0), (3, 3))
