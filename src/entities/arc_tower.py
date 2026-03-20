from src.entities.tower import Tower


class ArcTower(Tower):
    """Íj Torony - nagy sebzés, lassú lövés."""
    
    def __init__(self, gx: int, gy: int) -> None:
        super().__init__(gx, gy)
        self.sebzes = 16  # Megnövelve 12-ről - DPS kiegyensúlyozás
        self.tuzelesi_sebesseg = 1500  # 1.5 másodperc
        self.hatotav = 3.0
        self.nev = "Íj Torony"

        self.base_sebzes = self.sebzes
        self.base_hatotav = self.hatotav
        self.base_tuzelesi_sebesseg = self.tuzelesi_sebesseg
    
    def _get_image_type(self) -> str:
        return "arc"
