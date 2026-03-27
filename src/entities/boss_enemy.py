import math
import pygame
from entities.enemy import Enemy
from entities.tower import Tower


class BossEnemy(Enemy):
    """Nagyobb, erősebb ellenség, aki a tornyokat is megtámadja."""

    def __init__(self, path: list[tuple[int, int]], wave: int = 1) -> None:
        # A boss nagyobb és erősebb, wave szerint skálázódik (HP +10% nehézítéshez)
        hp: int = 396 + wave * 30  # 360 -> 396 (+10%)
        speed: float = 0.8
        radius: int = 22
        color: tuple[int, int, int] = (150, 0, 150)

        super().__init__(path, speed, hp, radius, color)

        self.wave: int = wave  # Mentjük a wave-számot a jutalmazáshoz
        self.attack_range: int = 60
        self.attack_damage: int = 25 + wave * 5
        self.attack_cooldown: int = 1200
        self.last_attack: int = 0

    def update(self, towers: list[Tower] | None = None) -> None:
        # Mozgás a standard Enemy logika szerint
        super().update()

        # A boss csak akkor támad, ha vannak towers a pályán
        if towers:
            self._attack_nearest_tower(towers)

    def get_reward(self) -> int:
        """Boss jutalma: HP alapú + wave szorzó"""
        return self.max_hp // 3 + 2 + (self.wave * 10)

    def _attack_nearest_tower(self, towers: list[Tower]) -> None:
        now: int = pygame.time.get_ticks()
        if now - self.last_attack < self.attack_cooldown:
            return

        closest_tower: Tower | None = None
        closest_dist: float = float("inf")

        for tower in towers:
            tx: int
            ty: int
            tx, ty = tower.get_pixel_center()
            dist: float = math.hypot(self.x - tx, self.y - ty)
            if dist < closest_dist:
                closest_dist = dist
                closest_tower = tower

        if closest_tower and closest_dist <= self.attack_range:
            destroyed: bool = closest_tower.take_damage(self.attack_damage)
            self.last_attack = now
            if destroyed:
                print("Boss elpusztította a tornyot!")

    def draw_shape(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0) -> None:
        pygame.draw.circle(surface, self.color, (int(self.x + offset_x), int(self.y + offset_y)), self.radius)
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x + offset_x), int(self.y + offset_y)), self.radius, 3)
