from src.entities.tower import Tower


class ShockTower(Tower):
    """Sokk Torony - kis sebzés, gyors lövés."""
    
    def __init__(self, gx: int, gy: int) -> None:
        super().__init__(gx, gy)
        self.sebzes = 5
        self.tuzelesi_sebesseg = 500  # 0.5 másodperc
        self.hatotav = 2.5
        self.nev = "Sokk Torony"

        self.base_sebzes = self.sebzes
        self.base_hatotav = self.hatotav
        self.base_tuzelesi_sebesseg = self.tuzelesi_sebesseg
    
    def _get_image_type(self) -> str:
        return "shock"
