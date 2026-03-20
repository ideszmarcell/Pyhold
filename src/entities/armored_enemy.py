import pygame
from src.entities.enemy import Enemy

# Új szín az 5. típushoz: Kék
VILAGOSKEK = (100, 149, 237)

class ArmoredEnemy(Enemy):
    def __init__(self, path):
        # Páncélzott ellenség: közepes sebesség, nagy élet (HP +15% nehézítéshez)
        super().__init__(path, speed=2.0, hp=21, radius=17, color=VILAGOSKEK)

    def get_reward(self):
        """Páncélzott ellenség jutalma: HP // 2 + 2 = 11 pénz (kiegyenlítéshez)"""
        return self.max_hp // 2 + 2

    def draw_shape(self, surface, offset_x=0, offset_y=0):
        # Az Armored ellenség egy háromszög (pajzs alakú)
        points = [
            (self.x + offset_x, self.y - self.radius - 5 + offset_y),  # Felső csúcs
            (self.x + self.radius + 5 + offset_x, self.y + self.radius + offset_y),   # Jobb alsó
            (self.x - self.radius - 5 + offset_x, self.y + self.radius + offset_y)    # Bal alsó
        ]
        pygame.draw.polygon(surface, self.color, points)
