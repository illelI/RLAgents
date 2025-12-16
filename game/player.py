import pygame

class Player:

    def __init__(self, screen):
        self.screen = screen
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    def get_position(self):
        return self.player_pos

    def move(self, dt):
        pygame.draw.circle(self.screen, "red", self.player_pos, 5)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.player_pos.y > 1:
            self.player_pos.y -= 300 * dt
        if keys[pygame.K_s] and self.player_pos.y < self.screen.get_height():
            self.player_pos.y += 300 * dt
        if keys[pygame.K_a] and self.player_pos.x > 0:
            self.player_pos.x -= 300 * dt
        if keys[pygame.K_d] and self.player_pos.x < self.screen.get_width() - 1:
            self.player_pos.x += 300 * dt