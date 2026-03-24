"""Game state management system."""
from enum import Enum


class GameMode(Enum):
    """Different game states."""
    START_SCREEN = "start_screen"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class GameStateManager:
    """Manages overall game state."""
    
    def __init__(self):
        self.current_mode = GameMode.START_SCREEN
        self.lives = 4
        self.is_muted = False
        self.tower_building_mode = False
        self.tower_upgrade_mode = False
        self.menu_mode = False
        self.is_wave_select_active = False
        self.continuous_waves = False
    
    def switch_to(self, mode: GameMode) -> None:
        """Switch to a different game mode."""
        self.current_mode = mode
    
    def toggle_tower_mode(self) -> None:
        """Toggle tower building mode."""
        self.tower_building_mode = not self.tower_building_mode
    
    def toggle_upgrade_mode(self) -> None:
        """Toggle tower upgrade mode."""
        self.tower_upgrade_mode = not self.tower_upgrade_mode
    
    def toggle_menu(self) -> None:
        """Toggle menu mode."""
        self.menu_mode = not self.menu_mode
    
    def toggle_mute(self) -> None:
        """Toggle mute."""
        self.is_muted = not self.is_muted
    
    def toggle_wave_select(self) -> None:
        """Toggle wave selection UI."""
        self.is_wave_select_active = not self.is_wave_select_active
    
    def toggle_continuous_waves(self) -> None:
        """Toggle automatic wave mode."""
        self.continuous_waves = not self.continuous_waves
    
    def lose_life(self) -> bool:
        """Lose a life. Returns True if game over."""
        self.lives -= 1
        if self.lives <= 0:
            self.current_mode = GameMode.GAME_OVER
            return True
        return False
    
    def reset(self) -> None:
        """Reset state for new game."""
        self.current_mode = GameMode.PLAYING
        self.lives = 4
        self.tower_building_mode = False
        self.tower_upgrade_mode = False
        self.menu_mode = False
        self.is_tower_mode = False
        self.is_upgrade_mode = False
        self.is_wave_select_active = False
        self.continuous_waves = False
        self.is_muted = False
    
    def is_playing(self) -> bool:
        """Check if game is active."""
        return self.current_mode == GameMode.PLAYING
