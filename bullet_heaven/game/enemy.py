import math

class Enemy:
     baseHP = 100
     baseSpeed = 100
     def __init__(self, position ,dt, minutes):
          self.position = position
          self.max_hp = self.calculateHP(minutes)
          self.hp = self.max_hp
          self.speed = self.calculateSpeed(dt, minutes)
          self.dmg = 10

     def calculateHP(self, minutes):
         return self.baseHP * (1.1 ** minutes)
    
     def calculateSpeed(self, dt, minutes):
         return self.baseSpeed * dt + 5 * dt * minutes
    
     def move(self, player, enemies):
          direction_x = player.position.x - self.position.x
          direction_y = player.position.y - self.position.y
          distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
          if distance == 0:
               return
          direction_x /= distance
          direction_y /= distance
          next_x = self.position.x + direction_x * self.speed
          next_y = self.position.y + direction_y * self.speed

          for enemy in enemies:
               if enemy is self:
                    continue
               dx = enemy.position.x - next_x
               dy = enemy.position.y - next_y
               dist = math.sqrt(dx * dx + dy * dy)
               if dist < 10:
                    return
          
          dx = player.position.x - next_x
          dy = player.position.y - next_y
          dist = math.sqrt(dx * dx + dy * dy)
          if dist < 10:
               player.take_dmg(self.dmg)
               return

          self.position.x = next_x
          self.position.y = next_y
               
     def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0