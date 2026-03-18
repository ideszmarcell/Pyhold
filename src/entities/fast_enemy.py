import pygame
from src.entities.enemy import Enemy, SARGA

class FastEnemy(Enemy):
    def __init__(self, path):
        # Gyors, kevés élet
        super().__init__(path, speed=5.0, hp=10, radius=12, color=SARGA)

    def draw_shape(self, surface, offset_x=0, offset_y=0):
        # ÚJ: A Gyors ellenség egy rombusz (4 pontból álló sokszög)
        points = [
            (self.x + offset_x, self.y - self.radius - 5 + offset_y), # Felső csúcs
            (self.x + self.radius + offset_x, self.y + offset_y),     # Jobb csúcs
            (self.x + offset_x, self.y + self.radius + 5 + offset_y), # Alsó csúcs
            (self.x - self.radius + offset_x, self.y + offset_y)      # Bal csúcs
        ]
        pygame.draw.polygon(surface, self.color, points)