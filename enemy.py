"""PyHold - Ellenség osztály."""

import random
import pygame
from entity import Entity
from vector2 import Vector2
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, RED


class Enemy(Entity):
    """Ellenség osztály - különböző típusú ellenségek."""

    def __init__(self, x, y, enemy_type="basic"):
        self.enemy_type = enemy_type
        self.setup_type(enemy_type)
        super().__init__(x, y, self._width, self._height, self._color)
        self.health = self._health
        self.speed = self._speed
        self.damage = self._damage
        self.score_value = self._score_value

    def setup_type(self, enemy_type):
        if enemy_type == "basic":
            self._width, self._height = 28, 28
            self._color = RED
            self._health = 30
            self._speed = 80
            self._damage = 10
            self._score_value = 10
        elif enemy_type == "fast":
            self._width, self._height = 22, 22
            self._color = (255, 140, 0)
            self._health = 15
            self._speed = 160
            self._damage = 5
            self._score_value = 20
        elif enemy_type == "tank":
            self._width, self._height = 38, 38
            self._color = (150, 30, 30)
            self._health = 80
            self._speed = 40
            self._damage = 25
            self._score_value = 30

    def update(self, dt, player_pos=None):
        if player_pos:
            direction = player_pos - self.pos
            if direction.magnitude() > 0:
                self.velocity = direction.normalize() * self.speed
        super().update(dt)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
