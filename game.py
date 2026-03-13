import pygame
from settings import SZELESSEG, MAGASSAG
from map import Palya
from src.entities.enemy import Enemy
from gazdasag import Gazdasag
from button import Button

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
        
        self.gazdasag: Gazdasag = Gazdasag()
        self.indito_gomb = Button(SZELESSEG - 200, 10, 180, 40, "HULLÁM INDÍTÁSA")
        
        self.utvonal = self.palya.kinyer_utvonal()
        self.ellensegek = []
        
        if self.utvonal:
            self.ellensegek.append(Enemy(self.utvonal))

    def esemenyek(self) -> None:
        """Kezeli a felhasználó eseményeit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.futo = False
                
            if self.indito_gomb.handle_event(event):
                if self.utvonal:
                    self.ellensegek.append(Enemy(self.utvonal))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.indito_gomb.hovered:
                        if self.gazdasag.vasarlas(100):
                            self.palya.cella_modositas(event.pos)

    def rajzol(self) -> None:
        """Képernyő frissítése"""
        self.palya.rajzol(self.ablak)
        
        for ellenseg in self.ellensegek:
            ellenseg.update()
            ellenseg.draw(self.ablak)
            
            if ellenseg.reached_end:
                self.ellensegek.remove(ellenseg)

        self.gazdasag.rajzol_ui(self.ablak, 2)
        self.indito_gomb.draw(self.ablak)

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