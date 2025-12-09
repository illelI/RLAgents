import pygame
from player import Player
from menu import Menu

def play(dt):
    screen.fill("white")
    player.move(dt)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill("white")
running = True
clock = pygame.time.Clock()
dt = 0

player = Player(screen)
menu = Menu(screen)

while running:
    dt = clock.tick(60) / 1000
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        menu.handle_events(event)
    if menu.play:
        play(dt)
    else:
        menu.draw()



pygame.quit()