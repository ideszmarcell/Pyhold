import pygame
from .enemy import Enemy

LIGHT_BLUE = (100, 149, 237)

class ArmoredEnemy(Enemy):
    def __init__(self, path: list[tuple[int, int]]) -> None:
        super().__init__(path, speed=2.0, hp=21, radius=17, color=LIGHT_BLUE)

    def get_reward(self) -> int:
        """Páncélzott ellenség jutalma: HP // 2 + 2 = 11 pénz (kiegyenlítéshez)"""
        return self.max_hp // 2 + 2

    def draw_shape(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0) -> None:
        # Az Armored ellenség egy háromszög (pajzs alakú)
        points: list[tuple[int, int]] = [
            (int(self.x + offset_x), int(self.y - self.radius - 5 + offset_y)),  # Felső csúcs
            (int(self.x + self.radius + 5 + offset_x), int(self.y + self.radius + offset_y)),   # Jobb alsó
            (int(self.x - self.radius - 5 + offset_x), int(self.y + self.radius + offset_y))    # Bal alsó
        ]
        pygame.draw.polygon(surface, self.color, points)
