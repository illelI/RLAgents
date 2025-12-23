import time
import pygame
import random
import threading
from enemy import Enemy

class Game:

    def __init__(self, player, screen, dt, seed=None):
        self.start_time = time.time()
        self.player = player
        self.screen = screen
        self.enemies = []
        self.dt = dt
        self.running = True
        if seed is not None:
            random.seed(seed)

        self.spawn_enemies_thread = threading.Thread(target=self.spawn_enemies)
        self.spawn_enemies_thread.daemon = True
        self.spawn_enemies_thread.start()

    def set_dt(self, dt):
        self.dt = dt

    def play(self, dt):
        self.player.move(dt)
        self.player.update_bullets(dt)
        self.player.draw_bullets()
        self.move_enemies()
        self.check_bullet_collisions()
        self.enemies_gc()
        self.show_timer()

    def show_timer(self):
        current_time = time.time() - self.start_time
        mins = int(current_time // 60)
        secs = int(current_time % 60)
        time_str = f"{mins:02}:{secs:02}"
        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(time_str, True, (79, 75, 75))
        text_surface.set_alpha(128)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(text_surface, text_rect)

    def spawn_enemies(self):
        while self.running:
            delay = -0.0011 * (time.time() - self.start_time) + 2
            x, y = 0, 0
            spawn_direction = random.randint(0, 3) #clockwise
            if spawn_direction == 0:
                y = -10
                x = random.randint(-10, self.screen.get_width() + 10)
            elif spawn_direction == 1:
                x = self.screen.get_width() + 10
                y = random.randint(-10, self.screen.get_height() + 10)
            elif spawn_direction == 2:
                y = self.screen.get_height() + 10
                x = random.randint(-10, self.screen.get_width() + 10)
            else:
                x = -10
                y = random.randint(-10, self.screen.get_height() + 10)

            self.enemies.append(Enemy(pygame.Vector2(x, y), self.dt, (time.time() - self.start_time)//60, self.screen))
            time.sleep(delay)
    
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