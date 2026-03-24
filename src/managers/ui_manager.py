"""UI management system."""
import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import Button
from ui.tower_selector import TowerSelector
from entities.tower import Tower


class UIManager:
    """Manages all UI elements."""
    
    def __init__(self):
        self.font_main = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 14, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 32, bold=True)
        

        self.select_wave_btn = Button(SCREEN_WIDTH - 200, 10, 190, 45)
        self.start_wave_btn = Button(SCREEN_WIDTH - 200, 60, 190, 45)
        self.towers_btn = Button(SCREEN_WIDTH - 200, 110, 190, 45)
        self.upgrade_btn = Button(SCREEN_WIDTH - 200, 160, 190, 45)
        self.menu_btn = Button(SCREEN_WIDTH - 200, 210, 190, 45)
        

        self.resume_btn = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 70, 180, 45)
        self.quit_btn = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 10, 180, 45)
        self.mute_btn = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 50, 180, 45)
        

        self.upgrade_confirm_btn = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 40, 180, 45)
        self.upgrade_cancel_btn = Button(SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 100, 180, 45)
        

        self.tower_selector = TowerSelector(Tower.TOWER_IMAGES, SCREEN_WIDTH, SCREEN_HEIGHT)
        

        self.wave_buttons = []
        self.wave_close_rect = None
    
    def get_all_buttons(self) -> list:
        """Get all game buttons for event handling."""
        return [
            self.select_wave_btn,
            self.start_wave_btn,
            self.towers_btn,
            self.upgrade_btn,
            self.menu_btn,
            self.resume_btn,
            self.quit_btn,
            self.mute_btn,
            self.upgrade_confirm_btn,
            self.upgrade_cancel_btn,
        ]
    
    def draw_hud(self, surface: pygame.Surface, money: int, lives: int) -> None:
        """Draw HUD panel with money and lives."""
        hud_w, hud_h = 320, 140
        hud_bg = pygame.Surface((hud_w, hud_h), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 180))
        surface.blit(hud_bg, (8, 8))
        pygame.draw.rect(
            surface, (255, 255, 255), (8, 8, hud_w, hud_h), 2, border_radius=8
        )
        
        money_text = self.font_main.render(f"Money: {money}", True, (255, 255, 255))
        surface.blit(money_text, (20, 16))
        
        lives_color = (255, 100, 100) if lives > 1 else (255, 50, 50)
        lives_text = self.font_main.render("♥" * max(0, lives), True, lives_color)
        surface.blit(lives_text, (20, 44))
    
    def draw_overlay(self, surface: pygame.Surface, alpha: int = 180) -> None:
        """Draw dark overlay for menus."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        surface.blit(overlay, (0, 0))
    
    def update_button_states(self, tower_mode: bool, upgrade_mode: bool, wave_running: bool, continuous: bool, has_boss: bool) -> None:
        """Update button visual states based on game state."""


        pass
