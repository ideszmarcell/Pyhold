from entities.tower import Tower


class ArcTower(Tower):
    """Íj Torony - nagy sebzés, lassú lövés."""
    
    def __init__(self, gx: int, gy: int) -> None:
        super().__init__(gx, gy)
        self.damage = 16  # Megnövelve 12-ről - DPS kiegyensúlyozás
        self.fire_speed = 1000  # 1 másodperc
        self.range = 3.0
        self.name = "arc Tower"

        self.base_damage = self.damage
        self.base_range = self.range
        self.base_fire_speed = self.fire_speed
    
    def _get_image_type(self) -> str:
        return "arc"
