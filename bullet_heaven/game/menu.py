import pygame

class Menu:
    class Button:
        def __init__(self, x, y, width, height, color, text, font, text_color):
            self.rect = pygame.Rect(x, y, width, height)
            self.color = color
            self.text = text
            self.font = font
            self.text_color = text_color

        def draw(self, screen):
            border_thickness = 5 
            border_color = (0, 0, 0)
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, border_color, self.rect, border_thickness)
            text = self.font.render(self.text, True, self.text_color)
            screen.blit(text, (self.rect.x + (self.rect.width - text.get_width()) // 2, 
                            self.rect.y + (self.rect.height - text.get_height()) // 2))

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)
        

    def __init__(self, screen):
        self.screen = screen
        self.play = False
        width, height = screen.get_size()

        self.playButton = Menu.Button(width/2 - 75, height/2 - 100, 150, 50, (255, 255, 255), "Play", pygame.font.Font(None, 36), (0, 0, 0))
        self.settingsButton = Menu.Button(width/2 - 75, height/2 - 25, 150, 50, (255, 255, 255), "Settings", pygame.font.Font(None, 36), (0, 0, 0))

    def draw(self):
        self.playButton.draw(self.screen)
        self.settingsButton.draw(self.screen)
    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.playButton.is_clicked(event.pos):
                self.play = True