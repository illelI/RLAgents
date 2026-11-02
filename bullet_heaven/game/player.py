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
    def __init__(self, pos_x, pos_y):
        self.max_hp = 100
        self.xp_to_next_lvl = 100
        self.stat_points = 0
        self.current_xp = 0
        self.xp_multiplier = 1
        self.hp = self.max_hp
        self.shoot_cooldown = 1
        self.dmg_cooldown = 1
        self.current_dmg_cooldown = 0
        self.shoot_timer = 0.0
        self.move_speed = 300
        self.hp_regen = 1
        self.regen_cooldown = 5.0
        self.dmg = 35
        self.bullets = []
        self.position = pygame.Vector2(pos_x, pos_y)
        self.aim_angle = 0.0
        self.isShooting = False
        self.move_dir = pygame.Vector2(0, 0)
        self.xp_collected = 0
        self.dmg_taken = 0
    
    def apply_action(self, action):
        move, aim, upgrade = action

        if self.stat_points != 0:
            self.upgradeStat(upgrade)

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
        self.position += self.move_dir * self.move_speed * dt
        self.position.x = max(0, min(1279, self.position.x))
        self.position.y = max(0, min(719, self.position.y))

    def shoot(self, dt):
        self.shoot_timer -= dt

        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_cooldown
            self.bullets.append(
                Bullet(
                    self.position.x,
                    self.position.y,
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
        self.current_dmg_cooldown -= dt
        self.regen(dt)
        self.move(dt)
        self.shoot(dt)
        self.update_bullets(dt)
    
    def regen(self, dt):
        self.regen_cooldown -= dt
        if self.regen_cooldown < 0:
            if self.hp + self.hp_regen < self.max_hp:
                self.hp += self.hp_regen
            else:
                self.hp = self.max_hp
            self.regen_cooldown = 5.0


    def take_dmg(self, dmg):
        if self.current_dmg_cooldown < 0:
            self.current_dmg_cooldown = self.dmg_cooldown 
            self.hp -= dmg
            self.dmg_taken += 1
        
    def get_xp(self):
        self.current_xp += 10 * self.xp_multiplier
        xp = self.current_xp - self.xp_to_next_lvl
        self.xp_collected += 1
        if xp >= 0:
            self.xp_to_next_lvl = self.xp_to_next_lvl * 1.1 + 10
            self.current_xp = xp
            self.stat_points += 1

    def upgradeStat(self, choosen):     
        self.stat_points -=1       
        if choosen == 1:
            self.move_speed *= 1.1
        elif choosen == 2:
            self.dmg *= 1.1
        elif choosen == 3:
            self.dmg_cooldown *= 1.1
        elif choosen == 4:
            self.max_hp *= 1.1
        elif choosen == 5:
            self.shoot_cooldown *= 0.9   
        elif choosen == 6:
            self.hp_regen += 1
        elif choosen == 7:
            self.xp_multiplier *= 1.1