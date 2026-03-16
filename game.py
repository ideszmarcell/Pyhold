import pygame
from settings import SZELESSEG, MAGASSAG, MAZE, AR_TORONY  # Itt a MAZE-t használd a pályához
from map import Palya

# Az új elérési út a mappaszerkezeted alapján:
from src.entities.basic_enemy import BasicEnemy
from src.entities.tank_enemy import TankEnemy
from src.entities.fast_enemy import FastEnemy
from src.entities.armored_enemy import ArmoredEnemy
from src.entities.boss_enemy import BossEnemy
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
        self.menu_gomb = Button(SZELESSEG - 190, 110, 180, 45)  # Menü gomb

        self.futo = True
        self.utvonal = self.palya.kinyer_utvonal()
        self.ellensegek = []
        self.hullam_szam = 0
        self.maradek_ellenseg = 0
        self.utolso_spawn = 0
        self.hullam_fut = False

        # Gazdaság
        self.penz = 200
        self.tower_costs = {
            "arc": AR_TORONY,
            "shock": AR_TORONY,
            "slow": AR_TORONY,
        }

        # Boss logika: minden wave végén jön egy boss
        self.boss: BossEnemy | None = None
        self.boss_spawned_wave: int = 0
        self.boss_pending: bool = False
        self.boss_spawn_delay_ms: int = 2000  # mennyi idő múlva spawnoljon a boss
        self.boss_spawn_ready_time: int = 0

        # Boss legyőzése utáni jutalom
        self.boss_reward: int = 150
        self.boss_defeated_wave: int = 0

        # Menü & játékállapot
        self.menu_active = False
        self.font = pygame.font.SysFont("Arial", 22, bold=True)

        # Menü gombok (pause menu)
        self.resume_button = Button(SZELESSEG // 2 - 90, MAGASSAG // 2 - 20, 180, 45)
        self.quit_button = Button(SZELESSEG // 2 - 90, MAGASSAG // 2 + 40, 180, 45)

        self.tornya_mod = False  # Tornyok módja

    def indit_hullam(self):
        # Nem indíthatunk új hullámot, amíg a boss életben van.
        if self.boss is not None:
            return

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

            if self.menu_gomb.handle_event(event):
                self.menu_active = not self.menu_active

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.menu_active = not self.menu_active

            if self.menu_active:
                # Menü módban csak a menü gombokat kezeljük
                if self.resume_button.handle_event(event):
                    self.menu_active = False
                if self.quit_button.handle_event(event):
                    self.futo = False
                continue

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
                            # Ellenőrizzük a költséget
                            cost = self.tower_costs.get(selected_image, AR_TORONY)
                            if self.penz >= cost:
                                self.penz -= cost
                                # Beállítsd az új képet a toronyhoz
                                # Az tower_selector.tower_gx az oszlop (c), tower_gy a sor (r)
                                self.palya.set_tower_image(
                                    self.tower_selector.tower_gy,
                                    self.tower_selector.tower_gx,
                                    selected_image,
                                )
                                # Automatikusan kapcsold ki a tornyok módot
                                self.tornya_mod = False
                            else:
                                print("Nincs elég pénz a torony megvásárlásához!")
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
        # Ha a menü aktív, akkor ne frissítsük tovább a játékot (pause)
        if self.menu_active:
            return

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

        # Boss spawnolása egy kis várakozás után (wave vége után)
        if (
            not self.hullam_fut
            and self.maradek_ellenseg == 0
            and len(self.ellensegek) == 0
            and self.hullam_szam > 0
            and self.boss_spawned_wave < self.hullam_szam
        ):
            if not self.boss_pending:
                self.boss_pending = True
                self.boss_spawn_ready_time = pygame.time.get_ticks() + self.boss_spawn_delay_ms

        if self.boss_pending and pygame.time.get_ticks() >= self.boss_spawn_ready_time:
            self.boss = BossEnemy(self.utvonal, wave=self.hullam_szam)
            self.ellensegek.append(self.boss)
            self.boss_spawned_wave = self.hullam_szam
            self.boss_pending = False

        # Boss és egyéb ellenségek update-elése
        for e in list(self.ellensegek):
            if isinstance(e, BossEnemy):
                e.update(self.palya.tornyok)
            else:
                e.update()

        # Halott vagy célba ért ellenségek eltávolítása
        self.ellensegek[:] = [
            e
            for e in self.ellensegek
            if e.hp > 0 and not getattr(e, "reached_end", False)
        ]

        # Ha a boss legyőzött, adj jutalmat és reseteljük a referenciát
        if self.boss is not None and self.boss not in self.ellensegek:
            if self.hullam_szam > self.boss_defeated_wave:
                self.penz += self.boss_reward
                self.boss_defeated_wave = self.hullam_szam
                print(f"Boss legyőzve: +{self.boss_reward} pénz (összesen: {self.penz})")
            self.boss = None

        # Halott tornyok eltávolítása
        for torony in list(self.palya.tornyok):
            if torony.hp <= 0:
                self.palya.remove_tower(torony)

        # Hullám vége ellenőrzés
        if self.maradek_ellenseg == 0 and len(self.ellensegek) == 0:
            self.hullam_fut = False

    def rajzol(self) -> None:
        self.palya.rajzol(self.ablak)

        # Tornyok rajzolása (HP sávval együtt)
        for torony in self.palya.tornyok:
            torony.rajzol(self.ablak)

        # Ellenségek rajzolása
        for e in self.ellensegek[:]:
            e.draw(self.ablak)

        # Pénz kijelzése
        penz_surf = self.font.render(f"Pénz: {self.penz}", True, (255, 255, 255))
        self.ablak.blit(penz_surf, (10, 10))

        # Gomb feliratának kezelése
        if self.boss is not None:
            szoveg = f"BOSS WAVE {self.hullam_szam} - DEFEND!"
            aktiv = False
        elif self.boss_pending:
            szoveg = "BOSS JÖN..."
            aktiv = False
        elif self.hullam_fut:
            szoveg = f"WAVE {self.hullam_szam} IN PROGRESS"
            aktiv = False
        else:
            szoveg = f"START WAVE {self.hullam_szam + 1}"
            aktiv = True

        self.hullam_gomb.draw(self.ablak, szoveg, aktiv)

        # Tornyok gomb felirata
        tornya_szoveg = "TORNYOK BE" if self.tornya_mod else "TORNYOK KI"
        self.tornya_gomb.draw(self.ablak, tornya_szoveg, True)

        # Menü gomb
        self.menu_gomb.draw(self.ablak, "MENÜ", True)

        # Torony képválasztó kirajzolása
        self.tower_selector.draw(self.ablak)

        # Menü overlay
        if self.menu_active:
            overlay = pygame.Surface((SZELESSEG, MAGASSAG), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.ablak.blit(overlay, (0, 0))

            menu_title = self.font.render("MENÜ", True, (255, 255, 255))
            menu_rect = menu_title.get_rect(center=(SZELESSEG // 2, MAGASSAG // 2 - 80))
            self.ablak.blit(menu_title, menu_rect)

            self.resume_button.draw(self.ablak, "Folytatás", True)
            self.quit_button.draw(self.ablak, "Kilépés", True)

        pygame.display.update()

    def run(self) -> None:
        while self.futo:
            self.esemenyek()
            self.update()
            self.rajzol()
            self.ora.tick(60)
