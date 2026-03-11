"""PyHold - Felszedethető tárgyak."""

import pygame
from entity import Entity
from settings import GREEN, YELLOW, WHITE


class Pickup(Entity):
    """Felszedethető tárgyak - gyógyítás, pajzs, pontok."""

    def __init__(self, x, y, pickup_type="health"):
        self.pickup_type = pickup_type
        color = GREEN if pickup_type == "health" else YELLOW if pickup_type == "shield" else WHITE
        super().__init__(x, y, 16, 16, color)
        self.lifetime = 8.0
        self.blink_time = 3.0

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

    def apply(self, player):
        if self.pickup_type == "health":
            player.health = min(player.max_health, player.health + 25)
        elif self.pickup_type == "shield":
            player.activate_shield(5)
        elif self.pickup_type == "score":
            player.score += 50
        self.alive = False

    def draw(self, surface):
        if self.alive:
            if self.lifetime < self.blink_time:
                if int(self.lifetime * 6) % 2 == 0:
                    return
            pygame.draw.rect(surface, self.color, self.get_rect())
            if self.pickup_type == "health":
                cx, cy = int(self.pos.x + 8), int(self.pos.y + 8)
                pygame.draw.line(surface, WHITE, (cx - 4, cy), (cx + 4, cy), 2)
                pygame.draw.line(surface, WHITE, (cx, cy - 4), (cx, cy + 4), 2)
