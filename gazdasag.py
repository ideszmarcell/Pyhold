# gazdasag.py
import pygame
from settings import FEKETE, FEHER, ZOLD, NARANCS, AR_BANYASZ, AR_TORONY

class Gazdasag:
    def __init__(self) -> None:
        self.kristaly: int = 200  # Kezdőtőke
        # Betűtípus a kiíráshoz
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", 24, bold=True)

    def vasarlas(self, ar: int) -> bool:
        """Levonja a pénzt, ha van elég. Visszatér True/False értékkel."""
        if self.kristaly >= ar:
            self.kristaly -= ar
            return True
        return False

    def rajzol_ui(self, felulet: pygame.Surface, aktualis_epulet: int) -> None:
        """Kirajzolja a pénzt és az éppen kiválasztott épületet."""
        # 1 = Bányász, 2 = Torony
        epulet_nev = f"Bányász ({AR_BANYASZ})" if aktualis_epulet == 1 else f"Torony ({AR_TORONY})"
        epulet_szin = ZOLD if aktualis_epulet == 1 else NARANCS

        szoveg_penz = self.font.render(f"Kristály: {self.kristaly}", True, FEHER)
        szoveg_epulet = self.font.render(f"Épít [TAB]: {epulet_nev}", True, epulet_szin)

        # Rárajzoljuk a képernyő bal felső sarkába (fekete háttérrel, hogy olvasható legyen)
        pygame.draw.rect(felulet, FEKETE, (5, 5, 250, 70)) 
        felulet.blit(szoveg_penz, (10, 10))
        felulet.blit(szoveg_epulet, (10, 40))