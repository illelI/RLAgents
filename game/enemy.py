

class Enemy:
    baseHP = 100
    baseSpeed = 100
    def __init__(self, dt, minutes):
          self.hp = self.calculateHP(minutes)
          self.speed = self.calculateSpeed(dt, minutes)

    def calculateHP(self, minutes):
         return self.baseHP * (1.1 ** minutes)
    
    def calculateSpeed(self, dt, minutes):
         return self.baseSpeed * dt + 5 * dt * minutes
    