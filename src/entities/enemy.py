import math
import pygame

RED = (255, 0, 0)
ZOLD = (0, 255, 0)

PATH = []

class Enemy:
    def __init__(self, path):
        self.path = path
        self.path_index = 0
        self.x, self.y = self.path[0]
        self.speed = 3
        self.radius = 15
        self.reached_end = False
        
        # --- ÚJ: Életpontok beállítása ---
        self.max_hp = 10
        self.hp = 10 

    def update(self):
        # Csak akkor mozogjon, ha még nem ért a pálya végére
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

    def draw(self, surface):
        # Ellenség kirajzolása egy piros körként
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)
        
        # --- ÚJ: Életerő csík kirajzolása az ellenség felett ---
        hp_bar_width = 30
        hp_bar_height = 5
        hp_ratio = self.hp / self.max_hp
        
        # Piros háttér (hiányzó élet)
        pygame.draw.rect(surface, RED, (self.x - hp_bar_width/2, self.y - self.radius - 12, hp_bar_width, hp_bar_height))
        # Zöld előtér (meglévő élet)
        if self.hp > 0:
            pygame.draw.rect(surface, ZOLD, (self.x - hp_bar_width/2, self.y - self.radius - 12, hp_bar_width * hp_ratio, hp_bar_height))