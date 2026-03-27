import pygame
from pygame import Surface
from entities.enemy import Enemy, YELLOW

class FastEnemy(Enemy):
    def __init__(self, path: list[tuple[int, int]]) -> None:
        super().__init__(path, speed=5.0, hp=11, radius=12, color=YELLOW)

    def get_reward(self) -> int:
        """Gyors ellenség jutalma: HP // 2 + 2 = 7 pénz (kiegyenlítéshez)"""
        return self.max_hp // 2 + 2

    def draw_shape(self, surface: Surface, offset_x: int = 0, offset_y: int = 0):
        # ÚJ: A Gyors ellenség egy rombusz (4 pontból álló sokszög)
        points: list[tuple[int, int]] = [
            (int(self.x + offset_x), int(self.y - self.radius - 5 + offset_y)), # Felső csúcs
            (int(self.x + self.radius + offset_x), int(self.y + offset_y)),     # Jobb csúcs
            (int(self.x + offset_x), int(self.y + self.radius + 5 + offset_y)), # Alsó csúcs
            (int(self.x - self.radius + offset_x), int(self.y + offset_y))      # Bal csúcs
        ]
        pygame.draw.polygon(surface, self.color, points)