"""PyHold - Hullámkezelő."""

import random
from enemy import Enemy
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class WaveManager:
    """Hullámkezelő - az ellenségek hullámokban érkeznek."""

    def __init__(self):
        self.wave_number = 0
        self.enemies = []
        self.spawn_timer = 0
        self.wave_active = False
        self.enemies_to_spawn = 0
        self.spawn_delay = 1.0
        self.wave_delay = 3.0
        self.wave_countdown = self.wave_delay

    def start_next_wave(self):
        self.wave_number += 1
        self.enemies_to_spawn = 3 + self.wave_number * 2
        self.wave_active = True
        self.spawn_timer = 0

    def get_enemy_type(self):
        roll = random.random()
        if self.wave_number >= 5 and roll < 0.15:
            return "tank"
        elif self.wave_number >= 3 and roll < 0.35:
            return "fast"
        return "basic"

    def spawn_enemy(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x = random.randint(0, SCREEN_WIDTH - 30)
            y = -30
        elif side == "bottom":
            x = random.randint(0, SCREEN_WIDTH - 30)
            y = SCREEN_HEIGHT + 5
        elif side == "left":
            x = -30
            y = random.randint(0, SCREEN_HEIGHT - 30)
        else:
            x = SCREEN_WIDTH + 5
            y = random.randint(0, SCREEN_HEIGHT - 30)

        enemy_type = self.get_enemy_type()
        return Enemy(x, y, enemy_type)

    def update(self, dt):
        if not self.wave_active:
            self.wave_countdown -= dt
            if self.wave_countdown <= 0:
                self.start_next_wave()
            return

        if self.enemies_to_spawn > 0:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                enemy = self.spawn_enemy()
                self.enemies.append(enemy)
                self.enemies_to_spawn -= 1
                self.spawn_timer = self.spawn_delay

        alive_enemies = [e for e in self.enemies if e.alive]
        self.enemies = alive_enemies
        if self.enemies_to_spawn <= 0 and len(alive_enemies) == 0:
            self.wave_active = False
            self.wave_countdown = self.wave_delay
