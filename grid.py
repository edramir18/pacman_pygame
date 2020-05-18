from typing import Dict, List

from cell import Cell
from coord import Coord


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = dict()  # type: Dict[Coord, Cell]
        for y in range(height):
            for x in range(width):
                coord = Coord(x, y)
                self.cells[coord] = Cell()

    def print_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                print(str(self.cells[Coord(x, y)]), end='')
            print('|')

    def get(self, pos):
        if isinstance(pos, Coord):
            x, y = pos.x, pos.y
        elif isinstance(pos, tuple) and len(pos) == 2:
            x, y = pos
        else:
            raise ValueError
        return self.cells.get(Coord(x, y))

    def get_neighbours(self, coord: Coord):
        pos_list = list()  # type: List[Coord]
        for adj in Coord.adjacency():
            pos = coord + adj
            if pos in self.cells:
                pos_list.append(pos)
        return pos_list
