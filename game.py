import random

from grid import Grid
from tetris_based_map_generator import TetrisBasedMapGenerator


class Game:
    def __init__(self, seed):
        print(seed)
        self.random = random.Random()
        self.random.seed(seed)
        self.grid = self.generate_grid()

    def generate_grid(self):
        width = self.random.randint(28, 33)
        height = self.random.randint(10, 15)
        if width % 2 == 0:
            width += 1
        grid = Grid(width, height)
        generator = TetrisBasedMapGenerator()
        generator.generate_horizontal_simetry(grid, self.random)
        return grid
