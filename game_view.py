import pygame as pg
from pygame.rect import Rect

from cell import Cell
from grid import Grid


class GameView:
    def __init__(self, game, tile_size):
        self.tile_size = tile_size
        self.half_tile = tile_size // 2
        self.height = (game.grid.height + 2) * tile_size
        self.width = (game.grid.width + 2) * tile_size
        self.window = pg.display.set_mode((self.width, self.height))
        self.wall_color = (0, 0, 0)
        self.floor_color = (255, 255, 255)

    def update(self, grid: Grid):
        rect = Rect(0, 0, self.width, self.height)
        pg.draw.rect(self.window, self.wall_color, rect, 0)
        for pos, cell in grid.cells.items():
            pos = pos * self.tile_size + self.tile_size
            rect = Rect(pos.x, pos.y, self.tile_size, self.tile_size)
            if cell.is_wall():
                pg.draw.rect(self.window, self.wall_color, rect, 0)
            else:
                pg.draw.rect(self.window, self.floor_color, rect, 0)
