import pygame
from player import Player
from menu import Menu
from game import Game

def play(dt, game, screen):
    screen.fill("white")
    game.play(dt)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill("white")
running = True
clock = pygame.time.Clock()
dt = 0

player = Player(screen, False)
menu = Menu(screen)
game = None

while running:
    dt = clock.tick(60) / 1000
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        menu.handle_events(event)
    if menu.play and game is None:
        game = Game(player, screen, dt)
    elif menu.play and game:
        game.set_dt(dt)
        play(dt, game, screen)
    else:
        menu.draw()



pygame.quit()