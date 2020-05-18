import random
from typing import Set, Dict, List
from _collections import deque

from cell import Cell
from coord import Coord
from grid import Grid
from tetris_piece import TetrisPiece


class TetrisBasedMapGenerator:
    def __init__(self):
        self.pieces = list()

        # ##
        # ##
        cells = set()
        cells.add(Coord(0, 0))
        cells.add(Coord(1, 0))
        cells.add(Coord(0, 1))
        cells.add(Coord(1, 1))
        self.pieces.append(TetrisPiece(cells))

        # #
        # ##
        cells = set()
        cells.add(Coord(0, 0))
        cells.add(Coord(0, 1))
        cells.add(Coord(1, 1))
        piece = TetrisPiece(cells)
        self.pieces.append(piece)
        self.pieces.append(self.flip_x(piece))
        self.pieces.append(self.flip_y(piece))
        self.pieces.append(self.transpose(piece))

        # #
        # ##
        # #
        cells = set()
        cells.add(Coord(0, 0))
        cells.add(Coord(0, 1))
        cells.add(Coord(1, 1))
        cells.add(Coord(0, 2))
        piece = TetrisPiece(cells)
        self.pieces.append(piece)
        self.pieces.append(self.flip_x(piece))
        self.pieces.append(self.transpose(piece))
        self.pieces.append(self.flip_y(self.transpose(piece)))

        #  #
        # ###
        #  #
        cells = set()
        cells.add(Coord(1, 0))
        cells.add(Coord(1, 1))
        cells.add(Coord(2, 1))
        cells.add(Coord(1, 2))
        cells.add(Coord(0, 1))
        piece = TetrisPiece(cells)
        self.pieces.append(piece)

        # #
        # ###
        cells = set()
        cells.add(Coord(0, 0))
        cells.add(Coord(0, 1))
        cells.add(Coord(1, 1))
        cells.add(Coord(2, 1))
        piece = TetrisPiece(cells)
        self.pieces.append(piece)
        self.pieces.append(self.flip_x(piece))
        self.pieces.append(self.flip_y(piece))
        self.pieces.append(self.flip_x(self.flip_y(piece)))
        self.pieces.append(self.flip_x(self.flip_y(self.transpose(piece))))
        self.pieces.append(self.transpose(piece))
        self.pieces.append(self.flip_y(self.transpose(piece)))
        self.pieces.append(self.flip_x(self.transpose(piece)))

    @staticmethod
    def flip(piece: TetrisPiece, func):
        result = set()
        for coord in piece.blocks:
            result.add(func(coord))
        return TetrisPiece(result)

    def flip_x(self, piece):
        return self.flip(piece,
                         lambda coord: Coord(piece.max_x - coord.x, coord.y))

    def flip_y(self, piece):
        return self.flip(piece,
                         lambda coord: Coord(coord.x, piece.max_y - coord.y))

    def transpose(self, piece):
        return self.flip(piece,
                         lambda coord: Coord(coord.y, coord.x))

    def generate_horizontal_simetry(self, grid: Grid, rand: random.Random):
        width = grid.width // 2 + 1
        height = grid.height
        mini_grid = Grid(width, height)
        self.generate(mini_grid, rand)
        for pos, cell in mini_grid.cells.items():
            grid.get(pos).clone(cell)
            pos = Coord(grid.width - pos.x - 1, pos.y)
            grid.get(pos).clone(cell)
        pos_list = [pos for pos, cell in grid.cells.items() if cell.is_floor()]
        islands = self.detect_islands(pos_list, grid)
        for island in islands:
            for coord in island:
                grid.get(coord).celltype = Cell.CellType.WALL

    @staticmethod
    def detect_islands(pos_list: List[Coord], grid: Grid):
        islands = list()  # type: List[List[Coord]]
        fifo = deque()  # type: deque[Coord]
        computed = set()  # type: Set[Coord]
        for first in pos_list:
            if first in computed:
                continue
            fifo.append(first)
            island = list()  # type: List[Coord]
            computed.add(first)
            island.append(first)
            while len(fifo) > 0:
                e = fifo.popleft()
                for coord in grid.get_neighbours(e):
                    if coord not in computed and grid.get(coord).is_floor():
                        fifo.append(coord)
                        computed.add(coord)
                        island.append(coord)
            islands.append(island)
        islands.sort(key=lambda x: len(x), reverse=True)
        return islands[1:]

    def generate(self, grid: Grid, rand: random.Random):
        width = grid.width // 2 + 1
        height = grid.height // 2 + 1
        pieces = dict()  # type: Dict[Coord, TetrisPiece]
        block_origin = dict()  # type: Dict[Coord, Coord]
        occupied = set()  # type: Set[Coord]
        for y in range(height):
            for x in range(width):
                pos = Coord(x, y)
                if pos not in occupied:
                    rand.shuffle(self.pieces)
                    opts = [p for p in self.pieces
                            if self.piece_fits(p, occupied, pos)]
                    if len(opts) > 1:
                        self.place_piece(pieces, block_origin,
                                         occupied, pos, opts[1])
        for y in range(1, height):
            for x in range(1, width):
                pos = Coord(x, y)
                origin = block_origin.get(pos, None)
                grid_pos = Coord(x, y) * 2 - 1
                if origin is not None:
                    piece = pieces.get(origin)
                    block = pos - origin
                    for delta in Coord.adjacency():
                        adj = block + delta
                        if adj not in piece.blocks:
                            for i in range(3):
                                if delta.x == 0:
                                    cell_pos = grid_pos + Coord(i - 1, delta.y)
                                else:
                                    cell_pos = grid_pos + Coord(delta.x, i - 1)
                                if cell_pos in grid.cells:
                                    cell = grid.get(cell_pos)
                                    cell.celltype = Cell.CellType.FLOOR

    @staticmethod
    def piece_fits(piece: TetrisPiece, occupied: Set[Coord], pos: Coord):
        for coord in piece.blocks:
            n_pos = coord + pos
            if n_pos in occupied:
                return False
        return True

    @staticmethod
    def place_piece(pieces: Dict[Coord, TetrisPiece],
                    block_origin: Dict[Coord, Coord],
                    occupied: Set[Coord],
                    pos: Coord, piece: TetrisPiece):
        pieces[pos] = piece
        for coord in piece.blocks:
            coord = coord + pos
            block_origin[coord] = pos
            occupied.add(coord)
