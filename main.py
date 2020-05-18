import pygame as pg

from game import Game
from game_view import GameView


def start():
    game = Game(100)
    game.generate_grid()
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
        view.update(game.grid)
        pg.display.flip()
    pg.quit()


if __name__ == '__main__':
    start()