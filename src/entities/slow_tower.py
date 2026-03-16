from src.entities.tower import Tower


class SlowTower(Tower):
    """Lassító Torony - közepes sebzés, lassító effekt."""
    
    def __init__(self, gx: int, gy: int) -> None:
        super().__init__(gx, gy)
        self.sebzes = 8
        self.tuzelesi_sebesseg = 800  # 0.8 másodperc
        self.hatotav = 3.0
        self.nev = "Lassító Torony"
    
    def _get_image_type(self) -> str:
        return "slow"
    
    def tuzel(self, celpont, most: int) -> None:
        """Sebzi az ellenséget és alkalmazz lassító effektet."""
        super().tuzel(celpont, most)
        # Lassító effekt: 40%-kal lelassít 2 másodpercig
        celpont.slow_effect = 40
        celpont.slow_duration = 2000
        celpont.slow_start = most
