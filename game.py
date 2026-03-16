import pygame
from settings import SZELESSEG, MAGASSAG, MAZE  # Itt a MAZE-t használd a pályához
from map import Palya

# Az új elérési út a mappaszerkezeted alapján:
from src.entities.enemy import Enemy
from src.entities.basic_enemy import BasicEnemy
from src.entities.tank_enemy import TankEnemy
from src.entities.fast_enemy import FastEnemy
from src.entities.armored_enemy import ArmoredEnemy
from src.entities.tower import Tower
from src.ui.tower_selector import TowerSelector
from button import Button


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.ablak = pygame.display.set_mode((SZELESSEG, MAGASSAG))
        self.ora = pygame.time.Clock()
        self.palya = Palya()

        # Tornyok képek inicializálása
        Tower.load_images()

        # Torony képválasztó UI
        self.tower_selector = TowerSelector(Tower.TOWER_IMAGES, SZELESSEG, MAGASSAG)

        # A gomb helye és mérete
        self.hullam_gomb = Button(SZELESSEG - 190, 10, 180, 45)
        self.tornya_gomb = Button(SZELESSEG - 190, 60, 180, 45)  # Tornyok gomb

        self.futo = True
        self.utvonal = self.palya.kinyer_utvonal()
        self.ellensegek = []
        self.hullam_szam = 0
        self.maradek_ellenseg = 0
        self.utolso_spawn = 0
        self.hullam_fut = False
        self.tornya_mod = False  # Tornyok módja

    def indit_hullam(self):
        if not self.hullam_fut and len(self.ellensegek) == 0:
            self.hullam_szam += 1
            # Növekvő számú ellenség: 8 + (hullám * 3)
            # Wave 1: 11, Wave 2: 14, Wave 3: 17, stb.
            self.maradek_ellenseg = 8 + (self.hullam_szam * 3)
            self.hullam_fut = True

    def esemenyek(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.futo = False

            if self.hullam_gomb.handle_event(event):
                self.indit_hullam()

            if self.tornya_gomb.handle_event(event):
                self.tornya_mod = not self.tornya_mod  # Tornyok mód ki-be kapcsolása

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Ha a torony képválasztó aktív, kezeld a kattintást
                    if self.tower_selector.active:
                        selected_image = self.tower_selector.handle_click(event.pos)
                        if selected_image:
                            # Beállítsd az új képet a toronyhoz
                            # Az tower_selector.tower_gx az oszlop (c), tower_gy a sor (r)
                            self.palya.set_tower_image(
                                self.tower_selector.tower_gy,
                                self.tower_selector.tower_gx,
                                selected_image,
                            )
                            # Automatikusan kapcsold ki a tornyok módot
                            self.tornya_mod = False
                    # Csak akkor hat a tornyokra, ha a mód aktív és nem gombra kattintottál
                    elif (
                        self.tornya_mod
                        and not self.hullam_gomb.is_hovered
                        and not self.tornya_gomb.is_hovered
                    ):
                        gx, gy = self.palya.koordinata_szamitas(event.pos)
                        # Ellenőrzid, hogy toronyra kattintottál-e
                        if (
                            0 <= gy < self.palya.sorok
                            and 0 <= gx < self.palya.oszlopok
                            and self.palya.adatok[gy][gx] == 2
                        ):
                            # Ellenőrizd, hogy ez a torony még nem módosított-e
                            if self.palya.get_tower_image(gy, gx) is None:
                                # Nyisd meg a képválasztót
                                self.tower_selector.show(gx, gy)
                            else:
                                # Ha már van kép, zárjon ki a módot
                                self.tornya_mod = False

    def update(self):
        # Ellenségek beküldése
        if self.hullam_fut and self.maradek_ellenseg > 0:
            most = pygame.time.get_ticks()
            if most - self.utolso_spawn > 800:
                if self.utvonal:
                    # Az 5 féle ellenség rotációja wave-k alapján
                    enemy_types = [BasicEnemy, FastEnemy, TankEnemy, ArmoredEnemy]
                    enemy_index = (self.maradek_ellenseg % 5) % len(enemy_types)
                    selected_enemy = enemy_types[enemy_index]
                    
                    self.ellensegek.append(selected_enemy(self.utvonal))
                self.maradek_ellenseg -= 1
                self.utolso_spawn = most

        # Tornyok sebzése
        for torony in self.palya.tornyok:
            torony.celpont_kereses(self.ellensegek)
        
        # Halott ellenségek eltávolítása
        self.ellensegek[:] = [e for e in self.ellensegek if e.hp > 0]

        # Hullám vége ellenőrzés
        if self.maradek_ellenseg == 0 and len(self.ellensegek) == 0:
            self.hullam_fut = False

    def rajzol(self) -> None:
        self.palya.rajzol(self.ablak)

        for e in self.ellensegek[:]:
            e.update()  # Itt lehet, hogy kell a dt, ha a te Enemy-d azt várja!
            e.draw(self.ablak)
            if hasattr(e, "reached_end") and e.reached_end:
                self.ellensegek.remove(e)

        # Gomb feliratának kezelése
        if self.hullam_fut:
            szoveg = f"WAVE {self.hullam_szam} IN PROGRESS"
            aktiv = False
        else:
            szoveg = f"START WAVE {self.hullam_szam + 1}"
            aktiv = True

        self.hullam_gomb.draw(self.ablak, szoveg, aktiv)

        # Tornyok gomb felirata
        tornya_szoveg = "TORNYOK BE" if self.tornya_mod else "TORNYOK KI"
        self.tornya_gomb.draw(self.ablak, tornya_szoveg, True)

        # Torony képválasztó kirajzolása
        self.tower_selector.draw(self.ablak)

        pygame.display.update()

    def run(self) -> None:
        while self.futo:
            self.esemenyek()
            self.update()
            self.rajzol()
            self.ora.tick(60)
