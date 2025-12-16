import pygame
import math

class Enemy:
    baseHP = 100
    baseSpeed = 100
    def __init__(self, position ,dt, minutes, screen):
          self.position = position
          self.hp = self.calculateHP(minutes)
          self.speed = self.calculateSpeed(dt, minutes)
          self.screen = screen

    def calculateHP(self, minutes):
         return self.baseHP * (1.1 ** minutes)
    
    def calculateSpeed(self, dt, minutes):
         return self.baseSpeed * dt + 5 * dt * minutes
    
    def move(self, player_pos):
          pygame.draw.rect(self.screen, "black", pygame.Rect(self.position.x - 5, self.position.y - 5, 10, 10))

          direction_x = player_pos.x - self.position.x
          direction_y = player_pos.y - self.position.y
          distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
          if distance != 0:
               direction_x /= distance
               direction_y /= distance
               self.position.x += direction_x * self.speed
               self.position.y += direction_y * self.speed
    