import math
import pygame

PIROS = (255, 0, 0)
ZOLD = (0, 255, 0)
LILA = (128, 0, 128)
SARGA = (255, 255, 0)

class Enemy:
    """Ez az általános ellenség osztály, minden ellenség ebből fog származni"""
    def __init__(self, path, speed, hp, radius, color):
        self.path = path
        self.path_index = 0
        self.x, self.y = self.path[0]
        
        self.speed = speed
        self.max_hp = hp
        self.hp = hp
        self.radius = radius
        self.color = color
        
        self.reached_end = False

    def update(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.hypot(dx, dy)

            if distance < self.speed:
                self.path_index += 1
                self.x, self.y = target_x, target_y
            else:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        else:
            self.reached_end = True

    def draw_shape(self, surface):
        """Alapértelmezett alakzat: egy kör. Ezt fogják felülírni a speciális ellenségek."""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def draw(self, surface):
        self.draw_shape(surface)
        
        hp_bar_width = 30
        hp_bar_height = 5
        hp_ratio = self.hp / self.max_hp
        
        pygame.draw.rect(surface, PIROS, (self.x - hp_bar_width/2, self.y - self.radius - 12, hp_bar_width, hp_bar_height))
        if self.hp > 0:
            pygame.draw.rect(surface, ZOLD, (self.x - hp_bar_width/2, self.y - self.radius - 12, hp_bar_width * hp_ratio, hp_bar_height))