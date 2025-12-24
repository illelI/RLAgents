import pygame
from player import Player
from menu import Menu
from game import Game
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from render.renderer import Renderer


def play(dt, game):
    game.play(dt)
    mins, secs = game.get_time()
    renderer.draw(player.get_position(), player.get_bullets(), game.get_enemies(), mins, secs)


pygame.init()
renderer = Renderer()
running = True
clock = pygame.time.Clock()
dt = 0

player = Player(640, 360, False)
#menu = Menu(screen)
game = None

while running:
    dt = clock.tick(60) / 1000
    #wpygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #menu.handle_events(event)
    #if menu.play and game is None:
    if game is None:
        game = Game(player, dt)
    #elif menu.play and game:
    else:
        game.set_dt(dt)
        play(dt, game)
    #else:
    #    menu.draw()



pygame.quit()