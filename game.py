import pygame
from settings import SZELESSEG, MAGASSAG
from map import Palya
from src.entities.enemy import Enemy

# pylint: disable=no-member


class Game:
    """Főbb játék logika osztály"""

    def __init__(self) -> None:
        pygame.init()
        self.ablak: pygame.Surface = pygame.display.set_mode((SZELESSEG, MAGASSAG))
        pygame.display.set_caption("Outhold Pálya Rendszer")
        self.ora: pygame.time.Clock = pygame.time.Clock()
        self.palya: Palya = Palya()
        self.futo: bool = True
        
        # 1. Töréspontok meghatározása (Sor, Oszlop) a MAZE alapján
        self.utvonal_cellak = [
            (1, 3),   # Kezdőpont
            (1, 16),  # Jobb felső sarok
            (4, 16),  # Jobb középső sarok
            (4, 5),   # Bal középső sarok
            (7, 5),   # Bal alsó sarok
            (7, 16),  # Jobb alsó sarok
            (10, 16), # Utolsó előtti sarok
            (10, 5)   # Cél
        ]
        
        # 2. Cellák átalakítása pixel koordinátákká (a cellák közepe)
        self.utvonal_pixelek = [
            (c * RACS_MERET + RACS_MERET // 2, r * RACS_MERET + RACS_MERET // 2)
            for r, c in self.utvonal_cellak
        ]

        # 3. Ellenségek listája (egyelőre csak 1 ellenséget adunk hozzá)
        self.ellensegek: list[Enemy] = [Enemy(self.utvonal_pixelek)]

    def esemenyek(self) -> None:
        """Kezeli a felhasználó eseményeit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.futo = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.palya.cella_modositas(event.pos)

    def frissit(self) -> None:
        """Játékállapot (pl. mozgás) frissítése"""
        for ellenseg in self.ellensegek:
            ellenseg.update()
            
        # Opcionális: Vegyük ki a listából azokat, akik célba értek
        self.ellensegek = [e for e in self.ellensegek if not e.reached_end]

    def rajzol(self) -> None:
        """Képernyő frissítése"""
        self.palya.rajzol(self.ablak)
        
        # Ellenségek kirajzolása a pálya felé
        for ellenseg in self.ellensegek:
            ellenseg.draw(self.ablak)
            
        pygame.display.update()

    def run(self) -> None:
        """Főciklus futtatása"""
        while self.futo:
            self.esemenyek()
            self.frissit() # <-- Mozgás logika hívása
            self.rajzol()
            self.ora.tick(60)

    def quit(self) -> None:
        """Főbb játék logika osztály"""
        pygame.quit()

