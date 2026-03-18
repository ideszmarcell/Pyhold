import pygame
from src.entities.enemy import Enemy, SARGA

class FastEnemy(Enemy):
    def __init__(self, path):
        # Gyors, kevés élet
        super().__init__(path, speed=5.0, hp=10, radius=12, color=SARGA)

    def draw_shape(self, surface):
        # ÚJ: A Gyors ellenség egy rombusz (4 pontból álló sokszög)
        points = [
            (self.x, self.y - self.radius - 5), # Felső csúcs
            (self.x + self.radius, self.y),     # Jobb csúcs
            (self.x, self.y + self.radius + 5), # Alsó csúcs
            (self.x - self.radius, self.y)      # Bal csúcs
        ]
        pygame.draw.polygon(surface, self.color, points)