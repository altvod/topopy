from unittest import TestCase

from topopy.primitives.tile import KeyTile
from topopy.primitives.topology import RectangularTopology

from topopy.primitives.movement import SimpleRectangularMovement
from topopy.serialization.topology import RectangularCharSerializer


class TestRectangularTopology(TestCase):
    def test_init(self):
        RectangularTopology([
            [KeyTile(0) for j in range(10)]
            for i in range(10)
        ])

        with self.assertRaises(ValueError):
            RectangularTopology([
                [KeyTile(0) for j in range(10)],
                [KeyTile(0) for j in range(10)],
                [KeyTile(0) for j in range(8)],
            ])

    def test_to_graph(self):
        topo = RectangularCharSerializer(
            tile_factory=KeyTile.from_key,
            topology_class=RectangularTopology
        ).deserialize((
            '..#\n'
            '.##\n'
            '...\n'
        ))

        loc = RectangularTopology.location_class
        graph = {
            loc(0, 0): {
                loc(0, 1): 1,
                loc(1, 0): 1,
            },
            loc(0, 1): {
                loc(0, 0): 1,
            },
            loc(1, 0): {
                loc(0, 0): 1,
                loc(2, 0): 1,
            },
            loc(2, 0): {
                loc(1, 0): 1,
                loc(2, 1): 1,
            },
            loc(2, 1): {
                loc(2, 0): 1,
                loc(2, 2): 1,
            },
            loc(2, 2): {
                loc(2, 1): 1,
            },
        }

        movement_strategy = SimpleRectangularMovement(
            diagonal=False,
            weight_map={('.', '.'): 1}
        )
        result_graph = topo.to_graph(movement_strategy=movement_strategy)
        self.assertEqual(result_graph, graph)

    def test_getitem(self):
        loc = RectangularTopology.location_class
        topo = RectangularCharSerializer(
            tile_factory=KeyTile.from_key,
            topology_class=RectangularTopology
        ).deserialize((
            '..#\n'
            '.#Q\n'
            '...\n'
        ))
        self.assertEqual(KeyTile.from_key('Q'), topo[loc(1, 2)])

    def test_setitem(self):
        loc = RectangularTopology.location_class
        topo = RectangularCharSerializer(
            tile_factory=KeyTile.from_key,
            topology_class=RectangularTopology
        ).deserialize((
            '..#\n'
            '.##\n'
            '...\n'
        ))
        topo[loc(1, 2)] = KeyTile.from_key('Q')
        self.assertEqual(KeyTile.from_key('Q'), topo.matrix[1][2])
