import random

from coord import Coord
from grid import Grid
from tetris_based_map_generator import TetrisBasedMapGenerator


class Game:
    def __init__(self, seed):
        print(seed)
        self.cherries = 4
        self.random = random.Random()
        self.random.seed(seed)
        self.grid = self.generate_grid()
        self.pacman_per_player = self.random.randint(2, 5)
        self.players = [
            [Coord(0, 0) for _ in range(self.pacman_per_player)]
            for _ in range(2)
        ]
        self.generate_pacman_and_cherries()

    def generate_pacman_and_cherries(self):
        free_cells = [pos for pos, cell in self.grid.cells.items()
                      if pos.x != self.grid.width // 2 and cell.is_floor()]
        self.random.shuffle(free_cells)
        left_cells = [pos for pos in free_cells if pos.x < self.grid.width // 2]
        i = 0
        while i < self.pacman_per_player:
            left_cell = Coord(left_cells[i].x, left_cells[i].y)
            right_cell = Coord(self.grid.width - 1 - left_cell.x, left_cell.y)
            left_player = self.random.randint(0, 1)
            right_player = (left_player + 1) % 2
            self.players[left_player][i] = left_cell
            self.players[right_player][i] = right_cell
            i += 1
        for j in range(self.cherries // 2):
            left_cell = Coord(left_cells[i + j].x, left_cells[i + j].y)
            right_cell = Coord(self.grid.width - 1 - left_cell.x, left_cell.y)
            self.grid.get(left_cell).has_cherry = True
            self.grid.get(right_cell).has_cherry = True
        players = set()
        for player in self.players:
            for pos in player:
                players.add(pos)
        for pos, cell in self.grid.cells.items():
            if cell.is_floor() and not cell.has_cherry and pos not in players:
                cell.has_pellet = True

    def generate_grid(self):
        width = self.random.randint(28, 33)
        height = self.random.randint(10, 15)
        if width % 2 == 0:
            width += 1
        grid = Grid(width, height)
        generator = TetrisBasedMapGenerator()
        generator.generate_horizontal_simetry(grid, self.random)
        return grid
