from entities.tower import Tower
from entities.enemy import Enemy


class SlowTower(Tower):
    """Lassító Torony - közepes sebzés, lassító effekt."""
    
    def __init__(self, gx: int, gy: int) -> None:
        super().__init__(gx, gy)
        self.damage = 10  # Megnövelve 7-ről - DPS optimalizálás
        self.fire_speed = 800  # 0.8 másodperc
        self.range = 3.0
        self.name = "slow Tower"

        self.base_damage = self.damage
        self.base_range = self.range
        self.base_fire_speed = self.fire_speed
    
    def _get_image_type(self) -> str:
        return "slow"
    
    def shoot(self, target: Enemy, now: int) -> None:
        """Sebzi az ellenséget és alkalmazz lassító effektet."""
        super().shoot(target, now)

        target.slow_effect = 40
        target.slow_duration = 2000
        target.slow_start = now
