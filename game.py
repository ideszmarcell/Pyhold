import pygame
from settings import SZELESSEG, MAGASSAG
from map import Palya
# Importáljuk az ellenséget a mappaszerkezeted alapján:
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
        
        # --- ÚJ RÉSZ: Ellenségek és útvonal inicializálása ---
        self.utvonal = self.palya.kinyer_utvonal()
        self.ellensegek = []
        
        # Ha találtunk útvonalat, létrehozunk egy teszt ellenséget
        if self.utvonal:
            self.ellensegek.append(Enemy(self.utvonal))

    def esemenyek(self) -> None:
        """Kezeli a felhasználó eseményeit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.futo = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.palya.cella_modositas(event.pos)

    def rajzol(self) -> None:
        """Képernyő frissítése"""
        self.palya.rajzol(self.ablak)
        for ellenseg in self.ellensegek[:]:
            ellenseg.update()
            ellenseg.draw(self.ablak)
            
            # Töröljük az ellenséget, ha végigért a pályán, VAGY ha elfogyott az élete (hp <= 0)
            if ellenseg.reached_end or ellenseg.hp <= 0:
                self.ellensegek.remove(ellenseg)

        pygame.display.update()
    def run(self) -> None:
        """Főciklus futtatása"""
        while self.futo:
            self.esemenyek()
            self.rajzol()
            self.ora.tick(60)

    def quit(self) -> None:
        """Játék bezárása"""
        pygame.quit()