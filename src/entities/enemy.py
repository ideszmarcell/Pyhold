import math
import pygame

RED = (255, 0, 0)

PATH = []

class Enemy:
    def __init__(self, path):
        self.path = path
        self.path_index = 0
        # Kezdőpozíció beállítása az első útpontra
        self.x, self.y = self.path[0]
        self.speed = 3
        self.radius = 15
        self.reached_end = False

    def update(self):
        # Csak akkor mozogjon, ha még nem ért a pálya végére
        if self.path_index < len(self.path) - 1:
            # A következő célpont meghatározása
            target_x, target_y = self.path[self.path_index + 1]

            # Távolság kiszámítása a jelenlegi pozíció és a célpont között
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.hypot(dx, dy)

            # Ha a sebességünknél közelebb vagyunk a ponthoz, akkor megérkeztünk
            if distance < self.speed:
                self.path_index += 1
                self.x, self.y = target_x, target_y
            else:
                # Kiszámoljuk az irányt (normalizálás) és mozgatjuk az ellenséget
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        else:
            self.reached_end = True

    def draw(self, surface):
        # Ellenség kirajzolása egy piros körként
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)