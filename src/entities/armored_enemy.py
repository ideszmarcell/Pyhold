import pygame
from src.entities.enemy import Enemy

# Új szín az 5. típushoz: Kék
VILAGOSKEK = (100, 149, 237)

class ArmoredEnemy(Enemy):
    def __init__(self, path):
        # Páncélzott ellenség: közepes sebesség, nagy élet
        super().__init__(path, speed=2.0, hp=18, radius=17, color=VILAGOSKEK)

    def draw_shape(self, surface):
        # Az Armored ellenség egy háromszög (pajzs alakú)
        points = [
            (self.x, self.y - self.radius - 5),  # Felső csúcs
            (self.x + self.radius + 5, self.y + self.radius),   # Jobb alsó
            (self.x - self.radius - 5, self.y + self.radius)    # Bal alsó
        ]
        pygame.draw.polygon(surface, self.color, points)
