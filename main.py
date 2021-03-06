import random
import pygame as pg

from game import Game
from game_view import GameView


def start():
    game = Game(random.randint(1, 100) * 100)
    pg.init()
    clock = pg.time.Clock()
    running = True
    view = GameView(game, 40)

    while running:
        clock.tick(60)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    running = False
        view.update(game)
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    start()