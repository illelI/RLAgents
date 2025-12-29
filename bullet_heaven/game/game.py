import pygame
import random
from enemy import Enemy

class Game:

    def __init__(self, player, dt, seed=None):
        self.start_time = 0.0
        self.player = player
        self.enemies = []
        self.dt = dt
        self.running = True
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.spawn_timer = 0.0
        if seed is not None:
            random.seed(seed)

    def set_dt(self, dt):
        self.dt = dt

    def get_enemies(self):
        return self.enemies
    
    def get_time(self):
        mins = int(self.elapsed_time // 60)
        secs = int(self.elapsed_time % 60)
        return mins, secs

    def update(self, dt):
        self.elapsed_time += dt
        self.spawn_timer += dt
        self.player.update(dt)
        self.spawn_enemies(dt)
        self.move_enemies()
        self.check_bullet_collisions()
        self.enemies_gc()

    def spawn_enemies(self, dt):
        delay = -0.0011 * self.elapsed_time + 2

        if self.spawn_timer >= delay:
            self.spawn_timer = 0.0

            spawn_direction = random.randint(0, 3)
            if spawn_direction == 0:
                pos = pygame.Vector2(random.randint(-10, 1290), -10)
            elif spawn_direction == 1:
                pos = pygame.Vector2(1290, random.randint(-10, 730))
            elif spawn_direction == 2:
                pos = pygame.Vector2(random.randint(-10, 1290), 730)
            else:
                pos = pygame.Vector2(-10, random.randint(-10, 730))

            level = int(self.elapsed_time // 60)
            self.enemies.append(Enemy(pos, dt, level))
        
    
    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move(self.player.get_position())

    def check_bullet_collisions(self):
        bullets_to_remove = []
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies:
                if bullet.check_collision(enemy):
                    enemy.take_damage(bullet.damage)
                    bullets_to_remove.append(bullet)
                    break
            
        for bullet in bullets_to_remove:
            if bullet in self.player.bullets:
                self.player.bullets.remove(bullet)

    def enemies_gc(self):
        for i in range(len(self.enemies) - 1, -1, -1):
            if self.enemies[i].hp <= 0:
                del self.enemies[i]