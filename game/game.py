import time
import pygame

class Game:

    def __init__(self, player, screen):
        self.start_time = time.time()
        self.player = player
        self.screen = screen

    def play(self, dt):
        self.player.move(dt)
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
