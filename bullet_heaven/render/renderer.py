import pygame

class Renderer:
    WIDTH = 1280
    HEIGHT = 720
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
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
    
    def __draw_xp(self, xps):
        for xp in xps:
            pygame.draw.rect(self.screen, "blue", pygame.Rect(xp.x - 5, xp.y - 5, 10, 10))

    def __draw_hud(self, player, mins, secs):
        self.__draw_timer(mins, secs)
        hp_str = f"{int(player.hp)}/{int(player.max_hp)}"
        font = pygame.font.SysFont(None, 36)
        xp_str = f"{int(player.current_xp)}/{int(player.xp_to_next_lvl)}"
        hp_surface = font.render(hp_str, True, (255, 0, 38))
        xp_surface = font.render(xp_str, True, (79, 75, 75))
        hp_rect = hp_surface.get_rect(center=(50, 10))
        xp_rect = xp_surface.get_rect(center=(50, 50))
        stats_font = pygame.font.SysFont(None, 18)
        stats_str = f"dmg: {player.dmg}\nspeed: {player.move_speed}\ndmg cd: {player.dmg_cooldown}\nshoot cd: {player.shoot_cooldown}"
        stats_lines = stats_str.split('\n')
        stats_surfaces = []
        for line in stats_lines:
            stats_surfaces.append(stats_font.render(line, True, (79, 75, 75)))
        stats_rects = []
        offset = 100
        for surface in stats_surfaces:
            stats_rect = surface.get_rect(center=(50, offset))
            stats_rects.append(stats_rect)
            offset+=20
        self.screen.blit(hp_surface, hp_rect)
        self.screen.blit(xp_surface, xp_rect)
        for surface, rect in zip(stats_surfaces, stats_rects):
            self.screen.blit(surface, rect)


    def render(self, player, enemies, xp, mins=0, secs=0):
        pygame.event.pump()
        pygame.display.flip()
        self.screen.fill("white")
        self.__draw_player(player.position)
        self.__draw_bullets(player.bullets)
        self.__draw_enemies(enemies)
        self.__draw_hud(player, mins, secs)
        self.__draw_xp(xp)


    def draw_button(self, text, rect, color):
        pygame.draw.rect(self.screen, color, rect)
        text_surface = pygame.font.SysFont(None, 24).render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def upgrade_window(self):
        rect_width = 450
        rect_height = 375
        rect_x = (self.WIDTH - rect_width) // 2
        rect_y = (self.HEIGHT - rect_height) // 2
        window_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        button_width = 150
        button_height = 50
        buttons = [
            pygame.Rect(window_rect.x + 50, window_rect.y + 50, button_width, button_height),
            pygame.Rect(window_rect.x + 250, window_rect.y + 50, button_width, button_height),
            pygame.Rect(window_rect.x + 50, window_rect.y + 125, button_width, button_height),
            pygame.Rect(window_rect.x + 250, window_rect.y + 125, button_width, button_height),
            pygame.Rect(window_rect.x + 50, window_rect.y + 200, button_width, button_height),
            pygame.Rect(window_rect.x + 250, window_rect.y + 200, button_width, button_height),
            pygame.Rect(window_rect.x + 150, window_rect.y + 275, button_width, button_height),
        ]

        pygame.draw.rect(self.screen, (0,30, 240), window_rect)
        self.draw_button("Speed +10%", buttons[0], (255, 0, 0))
        self.draw_button("DMG +10%", buttons[1], (255, 0, 0))
        self.draw_button("DMG CD +10%", buttons[2], (255, 0, 0))
        self.draw_button("HP +10%", buttons[3], (255, 0, 0))
        self.draw_button("Shoot CD -10%", buttons[4], (255, 0, 0))
        self.draw_button("HP regen +1", buttons[5], (255, 0, 0))
        self.draw_button("XP gain +10%", buttons[6], (255, 0, 0))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, button in enumerate(buttons):
                        if button.collidepoint(pos):
                            return i+1

    def close(self):
        pygame.quit()