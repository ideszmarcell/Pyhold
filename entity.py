"""PyHold - Alap entitás osztály."""

import pygame
from vector2 import Vector2


class Entity:
    """Alap entitás osztály - minden játékbeli objektum ebből származik."""

    def __init__(self, x, y, width, height, color):
        self.pos = Vector2(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.alive = True
        self.velocity = Vector2(0, 0)

    def get_rect(self):
        return pygame.Rect(int(self.pos.x), int(self.pos.y), self.width, self.height)

    def update(self, dt):
        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.get_rect())

    def collides_with(self, other):
        return self.get_rect().colliderect(other.get_rect())
