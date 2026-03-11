"""PyHold - Játékos osztály."""

import pygame
from entity import Entity
from bullet import Bullet
from vector2 import Vector2
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, YELLOW


class Player(Entity):
    """A játékos karaktere, amit a felhasználó irányít."""

    def __init__(self, x, y):
        super().__init__(x, y, 32, 32, BLUE)
        self.speed = 200
        self.health = 100
        self.max_health = 100
        self.score = 0
        self.shield_active = False
        self.shield_timer = 0
        self.bullets = []
        self.shoot_cooldown = 0
        self.shoot_delay = 0.25

    def handle_input(self, keys, dt):
        self.velocity = Vector2(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed

        if self.velocity.magnitude() > 0:
            self.velocity = self.velocity.normalize() * self.speed

    def shoot(self, direction):
        if self.shoot_cooldown <= 0:
            bullet_x = self.pos.x + self.width // 2 - 3
            bullet_y = self.pos.y + self.height // 2 - 3
            bullet = Bullet(bullet_x, bullet_y, direction)
            self.bullets.append(bullet)
            self.shoot_cooldown = self.shoot_delay

    def update(self, dt):
        super().update(dt)

        self.pos.x = max(0, min(SCREEN_WIDTH - self.width, self.pos.x))
        self.pos.y = max(0, min(SCREEN_HEIGHT - self.height, self.pos.y))

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False

        for bullet in self.bullets[:]:
            bullet.update(dt)
            if not bullet.alive:
                self.bullets.remove(bullet)

    def take_damage(self, amount):
        if not self.shield_active:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.alive = False

    def activate_shield(self, duration=3):
        self.shield_active = True
        self.shield_timer = duration

    def draw(self, surface):
        super().draw(surface)
        if self.shield_active:
            shield_rect = self.get_rect().inflate(8, 8)
            pygame.draw.rect(surface, YELLOW, shield_rect, 2)

        for bullet in self.bullets:
            bullet.draw(surface)
