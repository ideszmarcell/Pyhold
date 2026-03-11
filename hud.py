"""PyHold - HUD (Heads-Up Display)."""

import pygame
from settings import (
    SCREEN_WIDTH, DARK_GRAY, RED, WHITE, YELLOW
)


class HUD:
    """Heads-Up Display - játék felület (élet, pontszám, stb.)."""

    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

    def draw(self, surface, player, wave_number):
        bar_width = 200
        bar_height = 20
        bar_x, bar_y = 10, 10
        health_ratio = player.health / player.max_health

        pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, RED, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)

        health_text = self.small_font.render(f"HP: {player.health}/{player.max_health}", True, WHITE)
        surface.blit(health_text, (bar_x + 5, bar_y + 2))

        score_text = self.font.render(f"Pont: {player.score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

        wave_text = self.font.render(f"Hullám: {wave_number}", True, YELLOW)
        surface.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, 10))

        if player.shield_active:
            shield_text = self.small_font.render(f"Pajzs: {player.shield_timer:.1f}s", True, YELLOW)
            surface.blit(shield_text, (10, 35))
