"""PyHold - Lövedék osztály."""

import pygame
from entity import Entity
from vector2 import Vector2
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, YELLOW


class Bullet(Entity):
    """Lövedék osztály a lövésekhez."""

    def __init__(self, x, y, direction):
        super().__init__(x, y, 6, 6, YELLOW)
        self.speed = 400
        self.direction = direction.normalize()
        self.velocity = self.direction * self.speed
        self.lifetime = 2.0

    def update(self, dt):
        super().update(dt)
        self.lifetime -= dt

        if (self.pos.x < -10 or self.pos.x > SCREEN_WIDTH + 10 or
            self.pos.y < -10 or self.pos.y > SCREEN_HEIGHT + 10 or
            self.lifetime <= 0):
            self.alive = False
