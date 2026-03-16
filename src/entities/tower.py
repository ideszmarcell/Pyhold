import pygame
import math
from settings import RACS_MERET, NARANCS, FEHER


class Tower:
    # Osztályszintű képek gyorsítótár
    _images_cache: dict[str, pygame.Surface] = {}

    TOWER_IMAGES = {
        "arc": "assets/images/arc_tower.png",
        "shock": "assets/images/shock_tower.png",
        "slow": "assets/images/slow_tower.png",
    }

    @classmethod
    def load_images(cls) -> None:
        """Előbetölti az összes torony képet."""
        for name, path in cls.TOWER_IMAGES.items():
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (RACS_MERET - 8, RACS_MERET - 8))
                cls._images_cache[name] = img
            except Exception as e:
                print(f"Hiba a {path} betöltésekor: {e}")

    def __init__(self, gx: int, gy: int, image_type: str = "arc") -> None:
        # Pozíció a rácson
        self.gx: int = gx
        self.gy: int = gy
        self.image_type: str = image_type  # Az aktuális kép típusa

        # Statisztikák (Clean Code: külön csoportosítva)
        self.hatotav: int = 3  # Rácsnyi távolság
        self.sebzes: int = 10
        self.tuzelesi_sebesseg: int = 1000  # Milliszekundum (1 mp)
        self.utolso_loves: int = 0

    def _get_pixel_kozep(self) -> tuple[int, int]:
        """Kiszámolja a torony közepének pixel koordinátáit."""
        px = self.gx * RACS_MERET + RACS_MERET // 2
        py = self.gy * RACS_MERET + RACS_MERET // 2
        return px, py

    def celpont_kereses(self, ellensegek: list) -> None:
        """Megkeresi a legközelebbi ellenséget a hatótávon belül."""
        most = pygame.time.get_ticks()
        if most - self.utolso_loves < self.tuzelesi_sebesseg:
            return

        torony_kozep = self._get_pixel_kozep()

        for ellenseg in ellensegek:
            # Távolság kiszámítása Pitagorasz-tétellel: a^2 + b^2 = c^2
            dx = ellenseg.x - torony_kozep[0]
            dy = ellenseg.y - torony_kozep[1]
            tavolsag = math.sqrt(dx**2 + dy**2)

            if tavolsag <= self.hatotav * RACS_MERET:
                self.tuzel(ellenseg, most)
                break

    def tuzel(self, celpont, most: int) -> None:
        """Sebzi az ellenséget és frissíti az időzítőt."""
        celpont.eletero -= self.sebzes
        self.utolso_loves = most
        # Itt később adhatunk hozzá lövés effektet (pl. egy vonalat)
        print(f"Torony ({self.gx}, {self.gy}) eltalálta az ellenséget!")

    def rajzol(self, ablak: pygame.Surface) -> None:
        """Kirajzolja a torony képét."""
        px = self.gx * RACS_MERET + 4
        py = self.gy * RACS_MERET + 4

        # Ha a kép nincs betöltve, rajzolj egy alapértelmezett négyzetet
        if self.image_type in self._images_cache:
            img = self._images_cache[self.image_type]
            ablak.blit(img, (px, py))
        else:
            # Fallback: narancs négyzet
            rect = (px, py, RACS_MERET - 8, RACS_MERET - 8)
            pygame.draw.rect(ablak, NARANCS, rect, border_radius=6)

            # Fehér kör a közepén
            kozep = self._get_pixel_kozep()
            pygame.draw.circle(ablak, FEHER, kozep, RACS_MERET // 5)
