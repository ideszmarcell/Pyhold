import pygame
import math
from enemy import Enemy # Feltételezzük, hogy az 'Enemy' osztály a 'enemy.py'-ban van
from settings import RACS_MERET # A rács méretére szükségünk lesz a pixel koordinátákhoz

# BossEnemy osztály
class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, utvonal: list):
        super().__init__()
        self.x = x
        self.y = y
        self.utvonal = utvonal
        self.utvonal_index = 0
        self.sebesseg = 0.5 # A boss lassabb, mint a normál ellenségek
        self.hp = 150 # A bossnak több HP-ja van
        self.max_hp = 150
        self.kep_meret = RACS_MERET * 2 # A boss nagyobb, mint a normál ellenségek
        self.kep = pygame.Surface((self.kep_meret, self.kep_meret), pygame.SRCALPHA)
        pygame.draw.circle(self.kep, (150, 0, 150), (self.kep_meret // 2, self.kep_meret // 2), self.kep_meret // 2)
        pygame.draw.circle(self.kep, (255, 0, 255), (self.kep_meret // 2, self.kep_meret // 2), self.kep_meret // 2 - 5, 2)
        
        # Spawnoláshoz szükséges változók
        self.utolso_spawn_ido = pygame.time.get_ticks()
        self.spawn_gyakorisag = 5000 # 5 másodpercenként spawnol
        self.spawnolt_ellensegek = [] # Ebbe kerülnek a boss által spawnolt ellenségek

    def update(self) -> None:
        """Frissíti a boss pozícióját és spawnol kisebb ellenségeket."""
        self._mozog()
        self._spawnol_ellenseget()

    def _mozog(self) -> None:
        """A boss mozgatása az útvonal mentén."""
        if self.utvonal_index < len(self.utvonal) - 1:
            cel_x, cel_y = self.utvonal[self.utvonal_index + 1]
            
            # Pixel koordinátákra alakítás
            cel_pixel_x = cel_x * RACS_MERET + RACS_MERET // 2
            cel_pixel_y = cel_y * RACS_MERET + RACS_MERET // 2

            jelenlegi_pixel_x = self.x
            jelenlegi_pixel_y = self.y

            # Irány számítása
            dx = cel_pixel_x - jelenlegi_pixel_x
            dy = cel_pixel_y - jelenlegi_pixel_y
            tavolsag = math.sqrt(dx**2 + dy**2)

            if tavolsag > self.sebesseg:
                self.x += (dx / tavolsag) * self.sebesseg
                self.y += (dy / tavolsag) * self.sebesseg
            else:
                self.x = cel_pixel_x
                self.y = cel_pixel_y
                self.utvonal_index += 1

    def _spawnol_ellenseget(self) -> None:
        """Kisebb ellenségeket spawnol bizonyos időközönként."""
        most = pygame.time.get_ticks()
        if most - self.utolso_spawn_ido > self.spawn_gyakorisag:
            # Spawnolunk egy normál ellenséget a boss aktuális pozícióján
            # Fontos: A spawnolt ellenségnek ugyanazt az útvonalat kell követnie
            # ezért átadjuk neki a boss útvonalának hátralévő részét.
            uj_ellenseg = Enemy(
                self.x, 
                self.y, 
                self.utvonal[self.utvonal_index:], # Az útvonal hátralévő része
                sebesseg=1.5, # Picit gyorsabb, mint a boss
                hp=16 # Kicsit több HP
            )
            self.spawnolt_ellensegek.append(uj_ellenseg)
            self.utolso_spawn_ido = most
            print("Boss spawnolt egy kisebb ellenséget!")

    def draw(self, screen) -> None:
        """Kirajzolja a bosst a képernyőre."""
        # Kirajzolja a boss képét
        screen.blit(self.kep, (self.x - self.kep_meret // 2, self.y - self.kep_meret // 2))

        # HP bar kirajzolása
        bar_width = self.kep_meret
        bar_height = 5
        hp_ratio = self.hp / self.max_hp
        current_hp_width = bar_width * hp_ratio

        hp_bar_x = self.x - bar_width // 2
        hp_bar_y = self.y - self.kep_meret // 2 - bar_height - 2

        pygame.draw.rect(screen, (255, 0, 0), (hp_bar_x, hp_bar_y, bar_width, bar_height)) # Piros háttér (teljes HP)
        pygame.draw.rect(screen, (0, 255, 0), (hp_bar_x, hp_bar_y, current_hp_width, bar_height)) # Zöld HP csík