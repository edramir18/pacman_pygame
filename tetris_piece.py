from typing import Set

from coord import Coord


class TetrisPiece:
    def __init__(self, cells: Set[Coord]):
        self.blocks = cells
        self.max_x = max([cell.x for cell in cells])
        self.max_y = max([cell.y for cell in cells])

    def __str__(self):
        return f'maxX:{self.max_x} maxY:{self.max_y} blocks:{str(self.blocks)}'

    def __repr__(self):
        piece = '|'
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                p = Coord(x, y)
                piece += '#' if p in self.blocks else ' '
            piece += '|'
        return piece
