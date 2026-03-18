import pygame
from src.entities.enemy import Enemy, LILA

class TankEnemy(Enemy):
    def __init__(self, path):
        # Lassú, sok élet
        super().__init__(path, speed=1.5, hp=60, radius=20, color=LILA)

    def draw_shape(self, surface, offset_x=0, offset_y=0):
        # ÚJ: A Tank egy négyzet ("kocka")
        rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        rect.center = (int(self.x + offset_x), int(self.y + offset_y))
        pygame.draw.rect(surface, self.color, rect)