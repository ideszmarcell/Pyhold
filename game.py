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
from game_over import GameOverScreen
from start_screen import StartScreen

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
        self.fejlesztes_gomb = Button(SZELESSEG - 190, 110, 180, 45)  # Fejlesztések gomb
        self.menu_gomb = Button(SZELESSEG - 190, 160, 180, 45)  # Menü gomb

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
        
        # Fejlesztés módja
        self.fejlesztes_mod = False
        self.selected_upgrade_tower = None
        
        # Fejlesztés gomb és vissza gomb
        self.upgrade_button = Button(SZELESSEG // 2 - 90, MAGASSAG // 2 + 40, 180, 45)
        self.deselect_button = Button(SZELESSEG // 2 - 90, MAGASSAG // 2 + 100, 180, 45)

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
        
        self.eletek = 4  # 4 ellenség érhet be
        self.game_over_screen = GameOverScreen()
        self.start_screen = StartScreen()

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

            if self.start_screen.active:
                action = self.start_screen.handle_event(event)
                if action == "start":
                    self.start_screen.active = False
                elif action == "quit":
                    self.futo = False
                continue

            if self.game_over_screen.active:
                action = self.game_over_screen.handle_event(event)
                if action == "restart":
                    self.__init__()  # Játék teljes újraindítása
                elif action == "quit":
                    self.futo = False
                continue  

            if self.menu_gomb.handle_event(event):
                self.menu_active = not self.menu_active

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.menu_active = not self.menu_active
                self.selected_upgrade_tower = None
                self.fejlesztes_mod = False

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
                if not self.tornya_mod:
                    self.tower_selector.hide()

            if self.fejlesztes_gomb.handle_event(event):
                self.fejlesztes_mod = not self.fejlesztes_mod  # Fejlesztések mód ki-be kapcsolása
                if not self.fejlesztes_mod:
                    self.selected_upgrade_tower = None

            # Fejlesztés módban kezeljük az upgrade gombokat
            if self.fejlesztes_mod and self.selected_upgrade_tower:
                if self.upgrade_button.handle_event(event):
                    upgrade_cost = self.selected_upgrade_tower.get_upgrade_cost()
                    if upgrade_cost > 0:
                        if self.penz >= upgrade_cost:
                            self.penz -= upgrade_cost
                            self.selected_upgrade_tower.fejlesztes()
                            print(f"Torony fejlesztve! Szint: {self.selected_upgrade_tower.level}")
                        else:
                            print(f"Nincs elég pénz! Szükséges: {upgrade_cost}, Van: {self.penz}")
                    else:
                        print("A torony már maximum szinten van!")
                
                if self.deselect_button.handle_event(event):
                    self.selected_upgrade_tower = None

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
                                self.palya.set_tower_image(
                                    self.tower_selector.tower_gy,
                                    self.tower_selector.tower_gx,
                                    selected_image,
                                )
                                # Automatikusan kapcsold ki a tornyok módot
                                self.tornya_mod = False
                            else:
                                print("Nincs elég pénz a torony megvásárlásához!")
                    # Torony kiválasztása (tornyok módban)
                    elif (
                        self.tornya_mod
                        and not self.hullam_gomb.is_hovered
                        and not self.tornya_gomb.is_hovered
                        and not self.fejlesztes_gomb.is_hovered
                        and not self.menu_gomb.is_hovered
                    ):
                        gx, gy = self.palya.koordinata_szamitas(event.pos)
                        if (
                            0 <= gy < self.palya.sorok
                            and 0 <= gx < self.palya.oszlopok
                            and self.palya.adatok[gy][gx] == 2
                        ):
                            if self.palya.get_tower_image(gy, gx) is None:
                                self.tower_selector.show(gx, gy)
                            else:
                                self.tornya_mod = False
                    # Torony kiválasztása fejlesztéshez
                    elif (
                        self.fejlesztes_mod
                        and not self.hullam_gomb.is_hovered
                        and not self.fejlesztes_gomb.is_hovered
                        and not self.menu_gomb.is_hovered
                    ):
                        gx, gy = self.palya.koordinata_szamitas(event.pos)
                        if (
                            0 <= gy < self.palya.sorok
                            and 0 <= gx < self.palya.oszlopok
                            and self.palya.adatok[gy][gx] == 2
                        ):
                            # Torony megkeresése
                            tower_at_pos = None
                            for tower in self.palya.tornyok:
                                if tower.gx == gx and tower.gy == gy:
                                    tower_at_pos = tower
                                    break
                            
                            if tower_at_pos:
                                self.selected_upgrade_tower = tower_at_pos
                            else:
                                # Nincsen torony helyén, deselect
                                self.selected_upgrade_tower = None

    def update(self):
        if self.start_screen.active or self.menu_active or self.game_over_screen.active:
            return
            
        # ... itt folytatódik a meglévő kódod ...

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
                # Elő a boss előtt: adjon 100 pénzt
                self.penz += 100
                print(f"Boss előtt: +100 pénz (összesen: {self.penz})")

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

        # --- Életvesztés és Game Over logika ---
        for e in self.ellensegek:
            if getattr(e, "reached_end", False):
                self.eletek -= 1
                if self.eletek <= 0:
                    self.game_over_screen.active = True

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
        if self.start_screen.active:
            self.start_screen.draw(self.ablak)
            pygame.display.update()
            return
        
        self.palya.rajzol(self.ablak)

        # Tornyok rajzolása (HP sávval együtt)
        for torony in self.palya.tornyok:
            torony.rajzol(self.ablak, self.palya.offset_x, self.palya.offset_y)

        # Ellenségek rajzolása
        for e in self.ellensegek[:]:
            e.draw(self.ablak, self.palya.offset_x, self.palya.offset_y)

        # Pénz kijelzése
        penz_surf = self.font.render(f"Pénz: {self.penz}", True, (255, 255, 255))
        self.ablak.blit(penz_surf, (10, 10))
        elet_szin = (255, 255, 255) if self.eletek > 1 else (255, 50, 50)
        elet_surf = self.font.render(f"Életek: {max(0, self.eletek)}", True, elet_szin)
        self.ablak.blit(elet_surf, (10, 40))

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

        # Fejlesztések gomb felirata
        fejlesztes_szoveg = "FEJL. BE" if self.fejlesztes_mod else "FEJL. KI"
        self.fejlesztes_gomb.draw(self.ablak, fejlesztes_szoveg, True)

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
            
        if self.game_over_screen.active:
            self.game_over_screen.draw(self.ablak, self.hullam_szam)

        # Fejlesztés menü overlay (ha egy torony kiválasztott)
        if self.fejlesztes_mod and self.selected_upgrade_tower:
            overlay = pygame.Surface((SZELESSEG, MAGASSAG), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.ablak.blit(overlay, (0, 0))

            # Torony információk
            tower = self.selected_upgrade_tower
            title = self.font.render(f"{tower.nev} - Level {tower.level}/{tower.max_level}", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SZELESSEG // 2, MAGASSAG // 2 - 100))
            self.ablak.blit(title, title_rect)

            # Jelenlegi statisztika
            stats_font = pygame.font.SysFont("Arial", 18)
            sebzes_text = stats_font.render(f"Sebzés: {tower.sebzes}", True, (255, 200, 0))
            hatotav_text = stats_font.render(f"Hatótáv: {tower.hatotav:.1f}", True, (255, 200, 0))
            speed_text = stats_font.render(f"Lövési sebesség: {tower.tuzelesi_sebesseg}ms", True, (255, 200, 0))
            
            self.ablak.blit(sebzes_text, (SZELESSEG // 2 - 100, MAGASSAG // 2 - 40))
            self.ablak.blit(hatotav_text, (SZELESSEG // 2 - 100, MAGASSAG // 2 - 10))
            self.ablak.blit(speed_text, (SZELESSEG // 2 - 100, MAGASSAG // 2 + 20))

            # Fejlesztés költsége
            upgrade_cost = tower.get_upgrade_cost()
            if upgrade_cost > 0:
                cost_text = self.font.render(f"Fejlesztés költsége: {upgrade_cost} pénz", True, (255, 100, 100))
                cost_rect = cost_text.get_rect(center=(SZELESSEG // 2, MAGASSAG // 2 + 60))
                self.ablak.blit(cost_text, cost_rect)
                
                # Gombok
                self.upgrade_button.draw(self.ablak, "Fejlesztés", True)
            else:
                cost_text = self.font.render("Maximum szint elérve!", True, (100, 255, 100))
                cost_rect = cost_text.get_rect(center=(SZELESSEG // 2, MAGASSAG // 2 + 60))
                self.ablak.blit(cost_text, cost_rect)
            
            self.deselect_button.draw(self.ablak, "Vissza", True)

        pygame.display.update()

    def run(self) -> None:
        while self.futo:
            self.esemenyek()
            self.update()
            self.rajzol()
            self.ora.tick(60)
