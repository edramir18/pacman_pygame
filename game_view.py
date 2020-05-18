import pygame as pg
from pygame.rect import Rect

from cell import Cell
from coord import Coord
from game import Game
from grid import Grid


class GameView:
    def __init__(self, game, tile_size):
        self.tile_size = tile_size
        self.half_tile = tile_size // 2
        self.cherry_size = int(tile_size * 0.3)
        self.pellet_size = int(tile_size * 0.1)
        self.player_size = int(tile_size * 0.4)
        self.height = (game.grid.height + 2) * tile_size
        self.width = (game.grid.width + 2) * tile_size
        self.window = pg.display.set_mode((self.width, self.height))
        self.wall_color = (0, 0, 0)
        self.floor_color = (255, 255, 255)
        self.pellet_color = (0, 165, 0)
        self.player_color = (255, 0, 0)
        self.enemy_color = (0, 0, 255)
        self.font = pg.font.SysFont('Sans Serif', 14)

    def update(self, game: Game):
        rect = Rect(0, 0, self.width, self.height)
        pg.draw.rect(self.window, self.wall_color, rect, 0)
        for pos, cell in game.grid.cells.items():
            p_rect = pos * self.tile_size + self.tile_size
            rect = Rect(p_rect.x, p_rect.y, self.tile_size, self.tile_size)
            if cell.is_wall():
                pg.draw.rect(self.window, self.wall_color, rect, 0)
            else:
                pg.draw.rect(self.window, self.floor_color, rect, 0)
            if cell.has_cherry:
                center = (pos + 1) * self.tile_size + self.half_tile
                pg.draw.circle(self.window, self.pellet_color,
                               (center.x, center.y), self.cherry_size, 0)
            elif cell.has_pellet:
                center = (pos + 1) * self.tile_size + self.half_tile
                pg.draw.circle(self.window, self.pellet_color,
                               (center.x, center.y), self.pellet_size, 0)
        for key, player in enumerate(game.players):
            for pos in player:
                center = (pos + 1) * self.tile_size + self.half_tile
                if key == 0:
                    pg.draw.circle(self.window, self.player_color,
                                   (center.x, center.y), self.player_size, 0)
                else:
                    pg.draw.circle(self.window, self.enemy_color,
                                   (center.x, center.y), self.player_size, 0)
