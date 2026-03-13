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
        # 1. Alakzat kirajzolása (ez fog változni típusonként)
        self.draw_shape(surface)
        
        # 2. Életerő csík kirajzolása (ez mindenkinek ugyanaz marad)
        hp_bar_width = 30
        hp_bar_height = 5
        hp_ratio = self.hp / self.max_hp
        
        pygame.draw.rect(surface, PIROS, (self.x - hp_bar_width/2, self.y - self.radius - 12, hp_bar_width, hp_bar_height))
        if self.hp > 0:
            pygame.draw.rect(surface, ZOLD, (self.x - hp_bar_width/2, self.y - self.radius - 12, hp_bar_width * hp_ratio, hp_bar_height))
            
class BasicEnemy(Enemy):
    def __init__(self, path):
        # Sima ellenség: marad a piros kör
        super().__init__(path, speed=3, hp=10, radius=15, color=PIROS)

class TankEnemy(Enemy):
    def __init__(self, path):
        # Lassú, sok élet
        super().__init__(path, speed=1.5, hp=30, radius=20, color=LILA)

    def draw_shape(self, surface):
        # ÚJ: A Tank egy négyzet ("kocka")
        rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        rect.center = (int(self.x), int(self.y))
        pygame.draw.rect(surface, self.color, rect)

class FastEnemy(Enemy):
    def __init__(self, path):
        # Gyors, kevés élet
        super().__init__(path, speed=5.0, hp=5, radius=12, color=SARGA)

    def draw_shape(self, surface):
        # ÚJ: A Gyors ellenség egy rombusz (4 pontból álló sokszög)
        points = [
            (self.x, self.y - self.radius - 5), # Felső csúcs
            (self.x + self.radius, self.y),     # Jobb csúcs
            (self.x, self.y + self.radius + 5), # Alsó csúcs
            (self.x - self.radius, self.y)      # Bal csúcs
        ]
        pygame.draw.polygon(surface, self.color, points)