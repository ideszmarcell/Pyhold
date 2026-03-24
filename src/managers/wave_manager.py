"""Wave management system."""


class WaveManager:
    """Manages game waves and difficulty scaling."""
    
    def __init__(self):
        self.current_wave = 0
        self.is_running = False
        self.remaining_enemies = 0
        self.spawn_time = 0
        self.last_spawn = 0
        

        self.health_multiplier = 1.0
        self.count_multiplier = 1.0
        self.boss_damage_multiplier = 1.0
    
    def start_wave(self, wave_number: int) -> None:
        """Start a new wave."""
        self.current_wave = wave_number
        self.is_running = True
        self._apply_scaling()
        self._calculate_enemy_count()
    
    def _apply_scaling(self) -> None:
        """Calculate scaling multipliers for current wave."""
        level = (self.current_wave - 1) // 5 + 1
        self.health_multiplier = 1.0 + (level - 1) * 0.15
        self.count_multiplier = 1.0 + (level - 1) * 0.1
        self.boss_damage_multiplier = 1.0 + (level - 1) * 0.2
    
    def _calculate_enemy_count(self) -> None:
        """Calculate how many enemies spawn in this wave."""
        is_boss_wave = self.current_wave % 5 == 0
        if is_boss_wave:
            self.remaining_enemies = 0  # Boss only
        else:
            base_count = 8 + (self.current_wave * 3)
            self.remaining_enemies = int(base_count * self.count_multiplier)
    
    def spawn_enemy(self) -> bool:
        """Check if should spawn next enemy. Returns True if spawned."""
        if self.remaining_enemies > 0:
            self.remaining_enemies -= 1
            return True
        return False
    
    def is_boss_wave(self) -> bool:
        """Check if current wave has a boss."""
        return self.current_wave > 0 and self.current_wave % 5 == 0
    
    def end_wave(self) -> None:
        """End the current wave."""
        self.is_running = False
        self.remaining_enemies = 0
    
    def get_scaling_info(self) -> tuple[float, float, float]:
        """Get current scaling info as (health_mult, count_mult, boss_damage_mult)."""
        return (self.health_multiplier, self.count_multiplier, self.boss_damage_multiplier)
