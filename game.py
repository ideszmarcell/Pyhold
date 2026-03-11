import pygame
from settings import SZELESSEG, MAGASSAG, Palya
from entities.tower import Tower  # 1. Importáljuk a torony osztályt

# pylint: disable=no-member

class Game:
    """Főbb játék logika osztály"""

    def __init__(self) -> None:
        pygame.init()
        self.ablak: pygame.Surface = pygame.display.set_mode((SZELESSEG, MAGASSAG))
        pygame.display.set_caption("Outhold Pálya Rendszer")
        self.ora: pygame.time.Clock = pygame.time.Clock()
        self.palya: Palya = Palya()
        
        # 2. Listák az objektumok tárolására
        self.tornyok: list[Tower] = []
        self.ellensegek: list = []  # Ide jönnek majd a zombik/ellenségek
        
        self.futo: bool = True

    def esemenyek(self) -> None:
        """Kezeli a felhasználó eseményeit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.futo = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bal klikk
                    # Kiszámoljuk a rács koordinátákat
                    gx, gy = self.palya.koordinata_szamitas(event.pos)
                    
                    # Ellenőrizzük, van-e már ott torony (hogy ne építsünk egymásra)
                    van_mar_itt_valami = any(t.gx == gx and t.gy == gy for t in self.tornyok)
                    
                    if not van_mar_itt_valami:
                        # 3. Új torony példányosítása és hozzáadása a listához
                        uj_torony = Tower(gx, gy)
                        self.tornyok.append(uj_torony)
                        # A pálya adatokban is jelölhetjük (opcionális, ha a palya.py-t használod rajzolásra)
                        self.palya.cella_modositas(event.pos)

    def rajzol(self) -> None:
        """Képernyő frissítése"""
        # Előbb a pályát rajzoljuk le (háttér)
        self.palya.rajzol(self.ablak)
        
        # 4. Minden torony kirajzolása
        for torony in self.tornyok:
            torony.rajzol(self.ablak)
            
        pygame.display.update()

    def update(self) -> None:
        """Játékállapot frissítése (logika)"""
        # 5. Minden toronynak megparancsoljuk, hogy keressen célpontot
        for torony in self.tornyok:
            torony.celpont_kereses(self.ellensegek)

    def run(self) -> None:
        """Főciklus futtatása"""
        while self.futo:
            self.esemenyek()
            self.update()  # Logikai frissítés (lövés, mozgás)
            self.rajzol()  # Megjelenítés
            self.ora.tick(60)

    def quit(self) -> None:
        """Játék bezárása"""
        pygame.quit()