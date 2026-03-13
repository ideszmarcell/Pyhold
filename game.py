import pygame
from settings import SZELESSEG, MAGASSAG, MAZE # Itt a MAZE-t használd a pályához
from map import Palya
# Az új elérési út a mappaszerkezeted alapján:
from src.entities.enemy import Enemy, BasicEnemy, TankEnemy, FastEnemy
from button import Button

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.ablak = pygame.display.set_mode((SZELESSEG, MAGASSAG))
        self.ora = pygame.time.Clock()
        self.palya = Palya()
        
        # A gomb helye és mérete
        self.hullam_gomb = Button(SZELESSEG - 190, 10, 180, 45)
        
        self.futo = True
        self.utvonal = self.palya.kinyer_utvonal()
        self.ellensegek = []
        self.hullam_szam = 0
        self.maradek_ellenseg = 0
        self.utolso_spawn = 0
        self.hullam_fut = False

    def indit_hullam(self):
        if not self.hullam_fut and len(self.ellensegek) == 0:
            self.hullam_szam += 1
            self.maradek_ellenseg = 5 + (self.hullam_szam * 2)
            self.hullam_fut = True

    def esemenyek(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.futo = False
            
            if self.hullam_gomb.handle_event(event):
                self.indit_hullam()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.hullam_gomb.is_hovered:
                    self.palya.cella_modositas(event.pos)

    def update(self):
        # Ellenségek beküldése
        if self.hullam_fut and self.maradek_ellenseg > 0:
            most = pygame.time.get_ticks()
            if most - self.utolso_spawn > 800:
                if self.utvonal:
                    self.ellensegek.append(BasicEnemy(self.utvonal))
                self.maradek_ellenseg -= 1
                self.utolso_spawn = most
        
        # Hullám vége ellenőrzés
        if self.maradek_ellenseg == 0 and len(self.ellensegek) == 0:
            self.hullam_fut = False

    def rajzol(self) -> None:
        self.palya.rajzol(self.ablak)
        
        for e in self.ellensegek[:]:
            e.update() # Itt lehet, hogy kell a dt, ha a te Enemy-d azt várja!
            e.draw(self.ablak)
            if hasattr(e, 'reached_end') and e.reached_end:
                self.ellensegek.remove(e)

        # Gomb feliratának kezelése
        if self.hullam_fut:
            szoveg = f"WAVE {self.hullam_szam} IN PROGRESS"
            aktiv = False
        else:
            szoveg = f"START WAVE {self.hullam_szam + 1}"
            aktiv = True

        self.hullam_gomb.draw(self.ablak, szoveg, aktiv)
        pygame.display.update()

    def run(self) -> None:
        while self.futo:
            self.esemenyek()
            self.update()
            self.rajzol()
            self.ora.tick(60)