import pygame

class Renderer:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill("white")

    def __draw_player(self, player_pos):
        pygame.draw.circle(self.screen, "red", player_pos, 5)

    def __draw_bullets(self, bullets):
        for bullet in bullets:
            pygame.draw.circle(self.screen, (0, 0, 0), (int(bullet.pos.x), int(bullet.pos.y)), 2)

    def __draw_enemies(self, enemies):
        for enemy in enemies:
            pygame.draw.rect(self.screen, "black", pygame.Rect(enemy.position.x - 5, enemy.position.y - 5, 10, 10))

    def __draw_timer(self, mins, secs):
        time_str = f"{mins:02}:{secs:02}"
        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(time_str, True, (79, 75, 75))
        text_surface.set_alpha(128)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(text_surface, text_rect)

    def draw(self, player_pos, bullets, enemies, mins, secs):
        pygame.display.flip()
        self.screen.fill("white")
        self.__draw_player(player_pos)
        self.__draw_bullets(bullets)
        self.__draw_enemies(enemies)
        self.__draw_timer(mins, secs)