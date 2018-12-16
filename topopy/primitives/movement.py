from typing import Optional

from .location import Location
from .tile import Tile, KeyTile


SQRT_2 = 2.0**0.5
SQRT_3 = 3.0**0.5


class MovementStrategy:
    def get_passability(self, from_tile: Tile, to_tile: Tile,
                        from_loc: Location, to_loc: Location) -> Optional[int]:
        raise NotImplemented


class SimpleRectangularMovement(MovementStrategy):
    """
    Simple movement that supports only ``KeyTile``
    """

    __slots__ = 'diff_map', 'weight_map'

    diff_map_diag = (None, 1, SQRT_2, SQRT_3)
    diff_map_no_diag = (None, 1, None, None)

    def __init__(self, diagonal=False, weight_map=None):
        if diagonal:
            self.diff_map = self.diff_map_diag
        else:
            self.diff_map = self.diff_map_no_diag

        self.weight_map = weight_map

    def get_passability(self, from_tile: KeyTile, to_tile: KeyTile,
                        from_loc: Location, to_loc: Location) -> Optional[int]:
        diff = 0
        for from_coord, to_coord in zip(from_loc, to_loc):
            diff += int(from_coord != to_coord)

        passability = self.diff_map[diff]
        if passability is not None:
            tile_weight = self.weight_map.get((from_tile.key, to_tile.key))
            if tile_weight is not None:
                return passability * tile_weight
