from unittest import TestCase

from topopy.primitives.tile import KeyTile

from topopy.primitives.topology import RectangularTopology
from topopy.serialization.topology import (
    RectangularCharSerializer, RectangularKeySerializer
)


class TestRectangularCharSerializer(TestCase):
    def test_deserialize(self):
        t = KeyTile.from_key
        matrix = [
            [t('.'), t('.'), t('#')],
            [t('.'), t('#'), t('#')],
            [t('.'), t('.'), t('.')],
        ]
        topo = RectangularCharSerializer().deserialize((
            '..#\n'
            '.##\n'
            '...\n'
        ))

        self.assertEqual(topo.matrix, matrix)

    def test_serialize(self):
        t = KeyTile.from_key
        topo = RectangularTopology([
            [t('.'), t('.'), t('#')],
            [t('.'), t('#'), t('#')],
            [t('.'), t('.'), t('.')],
        ])
        str_matrix = (
            '..#\n'
            '.##\n'
            '...\n'
        )
        self.assertEqual(
            RectangularCharSerializer().serialize(topo).strip(),
            str_matrix.strip()
        )


class TestRectangularKeySerializer(TestCase):
    def test_deserialize(self):
        t = KeyTile.from_key
        matrix = [
            [t(0), t(0), t(1)],
            [t(0), t(1), t(1)],
            [t(0), t(0), t(0)],
        ]
        topo = RectangularKeySerializer().deserialize([
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 0],
        ])

        self.assertEqual(topo.matrix, matrix)

    def test_serialize(self):
        t = KeyTile.from_key
        topo = RectangularTopology([
            [t(0), t(0), t(1)],
            [t(0), t(1), t(1)],
            [t(0), t(0), t(0)],
        ])
        matrix = [
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 0],
        ]
        self.assertEqual(RectangularKeySerializer().serialize(topo), matrix)
