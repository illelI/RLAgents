import pygame
from player import Player
from game import Game
import math
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from render.renderer import Renderer

def aim(player_pos):
    mouse_pos = pygame.mouse.get_pos()
    dx = mouse_pos[0] - player_pos[0]
    dy = mouse_pos[1] - player_pos[1]
    angle = math.atan2(dy, dx)
    if angle < 0:
        angle += 2 * math.pi
    return angle

def quantize_angle(angle, directions=32):
    sector_size = 2 * math.pi / directions
    index = int((angle + sector_size / 2) // sector_size) % directions
    return index

def get_move(player):
    keys = pygame.key.get_pressed()
    x, y = 0, 0
    if keys[pygame.K_w] and player.player_pos.y > 1:
        y = -1
    if keys[pygame.K_s] and player.player_pos.y < 720:
        y = 1
    if keys[pygame.K_a] and player.player_pos.x > 0:
        x = -1
    if keys[pygame.K_d] and player.player_pos.x < 1279:
        x = 1
    idx = 0
    if x == 0 and y == -1:
        idx = 1
    elif x == 1 and y == -1:
        idx = 2
    elif x == 1 and y == 0:
        idx = 3
    elif x == 1 and y == 1:
        idx = 4
    elif x == 0 and y == 1:
        idx = 5
    elif x == -1 and y == 1:
        idx = 6
    elif x == -1 and y == 0:
        idx = 7
    elif x == -1 and y == -1:
        idx = 8
    return idx

def play(dt, game):
    move = get_move(game.player)
    aim_index = quantize_angle(aim(game.player.player_pos))
    action = [move, aim_index]
    game.player.apply_action(action)
    game.update(dt)
    mins, secs = game.get_time()
    renderer.render(player.get_position(), player.get_bullets(), game.get_enemies(), mins, secs)


renderer = Renderer()
running = True
clock = pygame.time.Clock()
dt = 0

player = Player(640, 360, False)
game = None

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if game is None:
        game = Game(player, dt)
    else:
        game.set_dt(dt)
        play(dt, game)


pygame.quit()