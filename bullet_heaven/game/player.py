import pygame
import threading
import time
import math

class Bullet:
    def __init__(self, x, y, angle, damage):
        self.pos = pygame.Vector2(x, y)
        self.angle = angle
        self.damage = damage

    def update(self, dt):
        self.pos.x += math.cos(self.angle) * 400 * dt
        self.pos.y += math.sin(self.angle) * 400 * dt

    def check_collision(self, enemy):
        distance = math.sqrt((self.pos.x - enemy.position.x) ** 2 + (self.pos.y - enemy.position.y) ** 2)
        return distance < 10

class Player:
    def __init__(self, pos_x, pos_y, isAgent):
        self.hp = 100
        self.shoot_speed = 1
        self.move_speed = 300
        self.dmg = 35
        self.bullets = []
        self.player_pos = pygame.Vector2(pos_x, pos_y)
        self.isAgent = isAgent
        self.aim_x, self.aim_y = 0, 0
        self.shoot_thread = threading.Thread(target=self.shoot)
        self.shoot_thread.daemon = True
        self.shoot_thread.start()

    def get_position(self):
        return self.player_pos
    
    def get_bullets(self):
        return self.bullets

    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.player_pos.y > 1:
            self.player_pos.y -= self.move_speed * dt
        if keys[pygame.K_s] and self.player_pos.y < 720:
            self.player_pos.y += self.move_speed * dt
        if keys[pygame.K_a] and self.player_pos.x > 0:
            self.player_pos.x -= self.move_speed * dt
        if keys[pygame.K_d] and self.player_pos.x < 1279:
            self.player_pos.x += self.move_speed * dt

    def shoot(self):
        while True:
            time.sleep(self.shoot_speed)
            if not self.isAgent:
                aim_x, aim_y = pygame.mouse.get_pos()
            else:
                aim_x, aim_y = self.aim_x, self.aim_y
            direction = pygame.Vector2(aim_x - self.player_pos.x, aim_y - self.player_pos.y)
            angle = math.atan2(direction.y, direction.x)
            self.bullets.append(Bullet(self.player_pos.x, self.player_pos.y, angle, self.dmg))

    def __is_bullet_on_screen(self, bullet):
        if bullet.pos.x < 0 or bullet.pos.x > 1280:
            return False
        if bullet.pos.y < 0 or bullet.pos.y > 720:
            return False
        return True

    def update_bullets(self, dt):
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if not self.__is_bullet_on_screen(bullet):
                self.bullets.remove(bullet)
