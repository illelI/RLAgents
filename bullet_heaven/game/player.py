import pygame
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
        return self.pos.distance_to(enemy.position) < 10

class Player:
    def __init__(self, pos_x, pos_y, isAgent):
        self.max_hp = 100
        self.hp = self.max_hp
        self.shoot_cooldown = 1
        self.shoot_timer = 0.0
        self.move_speed = 300
        self.dmg = 35
        self.bullets = []
        self.player_pos = pygame.Vector2(pos_x, pos_y)
        self.aim_angle = 0.0
        self.isShooting = False
        self.move_dir = pygame.Vector2(0, 0)
        self.isAgent = isAgent

    def get_position(self):
        return self.player_pos
    
    def get_bullets(self):
        return self.bullets
    
    def apply_action(self, action):
        move, aim = action
        directions = [
            (0, 0),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1)
        ]

        dx, dy = directions[move]
        self.move_dir = pygame.Vector2(dx, dy)
        if self.move_dir.length() > 0:
            self.move_dir = self.move_dir.normalize()
        self.aim_angle = (aim / 32) * 2 * math.pi

    def move(self, dt):
        self.player_pos += self.move_dir * self.move_speed * dt
        self.player_pos.x = max(0, min(1279, self.player_pos.x))
        self.player_pos.y = max(0, min(719, self.player_pos.y))

    def shoot(self, dt):
        self.shoot_timer -= dt

        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_cooldown
            self.bullets.append(
                Bullet(
                    self.player_pos.x,
                    self.player_pos.y,
                    self.aim_angle,
                    self.dmg
                )
            )

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

    def update(self, dt):
        self.move(dt)
        self.shoot(dt)
        self.update_bullets(dt)