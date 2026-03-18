import pygame
import math
from settings import RACS_MERET, NARANCS, FEHER


class Tower:
    """Alapozó Tower osztály - az összes torony ebből származik."""
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

    def __init__(self, gx: int, gy: int) -> None:
        """Alapozó konstruktor - felülírható leszármazottakban."""
        self.gx: int = gx
        self.gy: int = gy
        self.image_type: str = self._get_image_type()

        # A torony lényegében 2x2 cellát foglal a pályán
        self.size: int = 2

        # Életerő (tornyok mostantól sebezhetőek)
        self.max_hp: int = 150
        self.hp: int = self.max_hp

        # Absztrakt attribútumok - felülírni kell leszármazottakban
        self.hatotav: float = 3.0
        self.sebzes: int = 10
        self.tuzelesi_sebesseg: int = 1000
        self.nev: str = "Torony"

        self.utolso_loves: int = 0

    def _get_image_type(self) -> str:
        """Visszaadja a torony típusát - felülírható leszármazottakban."""
        return "arc"

    def _get_pixel_kozep(self) -> tuple[int, int]:
        """Kiszámolja a torony közepének pixel koordinátáit."""
        # A torony 2x2 cellát foglal, ezért a középpontot ennek megfelelően számoljuk.
        px = self.gx * RACS_MERET + (self.size * RACS_MERET) // 2
        py = self.gy * RACS_MERET + (self.size * RACS_MERET) // 2
        return px, py

    def celpont_kereses(self, ellensegek: list) -> None:
        """Megkeresi a legközelebbi ellenséget a hatótávon belül."""
        most = pygame.time.get_ticks()
        if most - self.utolso_loves < self.tuzelesi_sebesseg:
            return

        torony_kozep = self._get_pixel_kozep()

        for ellenseg in ellensegek:
            # Távolság kiszámítása
            dx = ellenseg.x - torony_kozep[0]
            dy = ellenseg.y - torony_kozep[1]
            tavolsag = math.sqrt(dx**2 + dy**2)

            if tavolsag <= self.hatotav * RACS_MERET:
                self.tuzel(ellenseg, most)
                break

    def tuzel(self, celpont, most: int) -> None:
        """Sebzi az ellenséget. Felülírható leszármazottakban."""
        celpont.hp -= self.sebzes
        self.utolso_loves = most
        print(f"{self.nev} ({self.gx}, {self.gy}) eltalálta az ellenséget! Sebzés: {self.sebzes}")

    def take_damage(self, damage: int) -> bool:
        """Sebzi a tornyot. Visszatér True-val, ha a torony megsemmisült."""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

        print(f"{self.nev} ({self.gx}, {self.gy}) sérült: -{damage} HP, hátralévő: {self.hp}")
        return self.hp == 0

    def rajzol(self, ablak: pygame.Surface, offset_x: int = 0, offset_y: int = 0) -> None:
        """Kirajzolja a torony képét és a HP-sávot."""
        px = self.gx * RACS_MERET + 4 + offset_x
        py = self.gy * RACS_MERET + 4 + offset_y

        img_width = self.size * RACS_MERET - 8
        img_height = self.size * RACS_MERET - 8

        if self.image_type in self._images_cache:
            img = self._images_cache[self.image_type]
            img = pygame.transform.scale(img, (img_width, img_height))
            ablak.blit(img, (px, py))
        else:
            # Fallback: narancs négyzet
            rect = (px, py, img_width, img_height)
            pygame.draw.rect(ablak, NARANCS, rect, border_radius=6)
            # Fehér kör a közepén
            kozep_x = self.gx * RACS_MERET + (self.size * RACS_MERET) // 2 + offset_x
            kozep_y = self.gy * RACS_MERET + (self.size * RACS_MERET) // 2 + offset_y
            pygame.draw.circle(ablak, FEHER, (kozep_x, kozep_y), RACS_MERET // 5)

        # Életerő sáv
        bar_width = img_width
        bar_height = 5
        hp_ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
        bar_x = px
        bar_y = py - bar_height - 2

        pygame.draw.rect(ablak, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(ablak, (0, 255, 0), (bar_x, bar_y, bar_width * hp_ratio, bar_height))
