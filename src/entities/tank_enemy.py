import pygame
from entities.enemy import Enemy, PURPLE

class TankEnemy(Enemy):
    def __init__(self, path: list[tuple[int, int]]) -> None:
        super().__init__(path, speed=1.5, hp=69, radius=20, color=PURPLE)

    def get_reward(self) -> int:
        """Tank ellenség jutalma: HP // 2 + 10 = 44 pénz (erősebb HP-val)"""
        return self.max_hp // 2 + 10

    def draw_shape(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        # ÚJ: A Tank egy négyzet ("kocka")
        rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        rect.center = (int(self.x + offset_x), int(self.y + offset_y))
        pygame.draw.rect(surface, self.color, rect)