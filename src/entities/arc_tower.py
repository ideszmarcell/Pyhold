from src.entities.tower import Tower


class ArcTower(Tower):
    """Íj Torony - nagy sebzés, lassú lövés."""
    
    def __init__(self, gx: int, gy: int) -> None:
        super().__init__(gx, gy)
        self.sebzes = 12
        self.tuzelesi_sebesseg = 1500  # 1.5 másodperc
        self.hatotav = 3.0
        self.nev = "Íj Torony"
    
    def _get_image_type(self) -> str:
        return "arc"
