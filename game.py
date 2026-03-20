import pygame
from settings import (
    SZELESSEG,
    MAGASSAG,
    MAZE,
    AR_TORONY,
)  # Itt a MAZE-t használd a pályához
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
        self.hullam_gomb = Button(SZELESSEG - 200, 10, 190, 45)
        self.wave_inditas_gomb = Button(
            SZELESSEG - 200, 60, 190, 45
        )  # Wave indítása (auto mode)
        self.tornya_gomb = Button(SZELESSEG - 200, 110, 190, 45)  # Tornyok gomb
        self.fejlesztes_gomb = Button(
            SZELESSEG - 200, 160, 190, 45
        )  # Fejlesztések gomb
        self.menu_gomb = Button(SZELESSEG - 200, 210, 190, 45)  # Menü gomb

        self.futo = True
        self.utvonal = self.palya.kinyer_utvonal()
        self.ellensegek = []
        self.hullam_szam = 0
        self.maradek_ellenseg = 0
        self.utolso_spawn = 0
        self.hullam_fut = False

        # Gazdaság
        self.penz = 175  # Csökkentve 200-ról - nehézítés
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

        # Wave selection és scaling system
        self.wave_select_active = False
        self.enemy_health_multiplier = 1.0
        self.enemy_count_multiplier = 1.0
        self.boss_damage_multiplier = 1.0
        self.wave_button_rects = []
        self.wave_close_rect = None
        self.continuous_waves = False  # Auto wave mode
        self.next_wave_auto_time = 0  # Mikor indítson új wavét automatikusan

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
        """Megnyitja a wave select menüt."""
        if self.boss is not None or self.hullam_fut:
            return
        self.wave_select_active = True

    def _calculate_scaling_for_wave(self, wave: int) -> tuple[float, float, float]:
        """Kiszámítja a scaling szorzókat az adott wave száma alapján."""
        level = (wave - 1) // 5 + 1  # Szint: 1-5
        health_mult = 1.0 + (level - 1) * 0.15
        count_mult = 1.0 + (level - 1) * 0.1
        boss_dmg_mult = 1.0 + (level - 1) * 0.2
        return health_mult, count_mult, boss_dmg_mult

    def _apply_scaling_for_wave(self, wave: int) -> None:
        """Alkalmazza a scaling szorzókat az adott wave-hez."""
        health_mult, count_mult, boss_dmg_mult = self._calculate_scaling_for_wave(wave)
        self.enemy_health_multiplier = health_mult
        self.enemy_count_multiplier = count_mult
        self.boss_damage_multiplier = boss_dmg_mult
        level = (wave - 1) // 5 + 1
        print(
            f"Wave {wave} (Szint {level}) scaling: HP: {health_mult:.2f}x, Szám: {count_mult:.2f}x, Boss DMG: {boss_dmg_mult:.2f}x"
        )

    def select_wave(self, wave_number: int) -> None:
        """Kiválasztott wave-t indítja el."""
        if self.boss is not None or self.hullam_fut or len(self.ellensegek) > 0:
            return

        self.hullam_szam = wave_number
        self.wave_select_active = False
        self._apply_scaling_for_wave(wave_number)

        # Boss wave ellenőrzés
        is_boss_wave = wave_number % 5 == 0
        if is_boss_wave:
            self.maradek_ellenseg = 0
        else:
            base_count = 8 + (wave_number * 3)
            self.maradek_ellenseg = int(base_count * self.enemy_count_multiplier)

        self.hullam_fut = True

    def start_continuous_waves(self, starting_wave: int = 1) -> None:
        """Auto wave mód bekapcsolása a megadott wave-től."""
        if self.continuous_waves:
            return  # Már fut
        self.continuous_waves = True
        self.hullam_szam = (
            starting_wave - 1
        )  # Hogy a következő select_wave automatikusan indul
        self.next_wave_auto_time = pygame.time.get_ticks() + 1000

    def stop_continuous_waves(self) -> None:
        """Auto wave mód kikapcsolása."""
        self.continuous_waves = False
        self.next_wave_auto_time = 0

    def _click_on_ui_buttons(self, pos: tuple[int, int]) -> bool:
        # Véletlen kattintás elkerülése a főképernyős toronyválasztásnál
        return (
            self.hullam_gomb.rect.collidepoint(pos)
            or self.wave_inditas_gomb.rect.collidepoint(pos)
            or self.tornya_gomb.rect.collidepoint(pos)
            or self.fejlesztes_gomb.rect.collidepoint(pos)
            or self.menu_gomb.rect.collidepoint(pos)
        )

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

            # Az overlay gombok handle_event-jét minden event-re meghívjuk
            if self.fejlesztes_mod and self.selected_upgrade_tower:
                self.upgrade_button.handle_event(event)
                self.deselect_button.handle_event(event)

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
                self.wave_select_active = False
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

            if self.wave_inditas_gomb.handle_event(event):
                # Wave indítása (automata) gomb
                if not self.continuous_waves:
                    self.start_continuous_waves(1)  # 1-es wavéről indít
                else:
                    self.stop_continuous_waves()

            if self.tornya_gomb.handle_event(event):
                self.tornya_mod = not self.tornya_mod  # Tornyok mód ki-be kapcsolása
                if not self.tornya_mod:
                    self.tower_selector.hide()

            if self.fejlesztes_gomb.handle_event(event):
                self.fejlesztes_mod = (
                    not self.fejlesztes_mod
                )  # Fejlesztések mód ki-be kapcsolása
                if not self.fejlesztes_mod:
                    self.selected_upgrade_tower = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos

                    # Wave select menü kezelése
                    if self.wave_select_active:
                        if self.wave_close_rect and self.wave_close_rect.collidepoint(
                            mouse_pos
                        ):
                            self.wave_select_active = False
                            continue

                        for btn_rect, wave_num in self.wave_button_rects:
                            if btn_rect.collidepoint(mouse_pos):
                                if self.continuous_waves:
                                    self.stop_continuous_waves()
                                self.select_wave(wave_num)
                                break
                        continue

                    # Ha UI gombok egyike alatt kattintunk, ne csináljunk további terepi eseményt
                    if self._click_on_ui_buttons(mouse_pos):
                        continue

                    # Az overlay gombok kezelése (már hívódtak a handle_event-jei)
                    if self.fejlesztes_mod and self.selected_upgrade_tower:
                        if self.deselect_button.is_hovered:
                            self.selected_upgrade_tower = None
                            continue

                        if self.upgrade_button.is_hovered:
                            upgrade_cost = (
                                self.selected_upgrade_tower.get_upgrade_cost()
                            )
                            if upgrade_cost > 0:
                                if self.penz >= upgrade_cost:
                                    self.penz -= upgrade_cost
                                    self.selected_upgrade_tower.fejlesztes()
                                    print(
                                        f"Torony fejlesztve! Szint: {self.selected_upgrade_tower.level}"
                                    )
                                else:
                                    print(
                                        f"Nincs elég pénz! Szükséges: {upgrade_cost}, Van: {self.penz}"
                                    )
                            else:
                                print("A torony már maximum szinten van!")
                            continue

                        # Többi kattintás nem fejlesztésre (csak overlay bezárása szükség esetén)
                        continue

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
                    elif self.tornya_mod and not self._click_on_ui_buttons(event.pos):
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
                    elif self.fejlesztes_mod and not self._click_on_ui_buttons(
                        event.pos
                    ):
                        gx, gy = self.palya.koordinata_szamitas(event.pos)
                        if (
                            0 <= gy < self.palya.sorok
                            and 0 <= gx < self.palya.oszlopok
                            and self.palya.adatok[gy][gx] == 2
                        ):
                            # Torony megkeresése - 2x2 terület kezelése
                            tower_at_pos = None
                            for tower in self.palya.tornyok:
                                # Torony 2x2 cellát foglal, ellenőrizni az összes cellát
                                if (
                                    tower.gx <= gx < tower.gx + tower.size
                                    and tower.gy <= gy < tower.gy + tower.size
                                ):
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

                    enemy = selected_enemy(self.utvonal)
                    # Scaling alkalmazása
                    enemy.hp = int(enemy.hp * self.enemy_health_multiplier)
                    enemy.max_hp = int(enemy.max_hp * self.enemy_health_multiplier)
                    self.ellensegek.append(enemy)
                self.maradek_ellenseg -= 1
                self.utolso_spawn = most

        # Tornyok sebzése
        for torony in self.palya.tornyok:
            torony.celpont_kereses(self.ellensegek)

        # Boss spawnolása egy kis várakozás után (csak boss wavéken)
        is_boss_wave = self.hullam_szam > 0 and self.hullam_szam % 5 == 0

        if (
            is_boss_wave
            and not self.hullam_fut
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
                self.boss_spawn_ready_time = (
                    pygame.time.get_ticks() + self.boss_spawn_delay_ms
                )

        if self.boss_pending and pygame.time.get_ticks() >= self.boss_spawn_ready_time:
            self.boss = BossEnemy(self.utvonal, wave=self.hullam_szam)
            # Scaling alkalmazása a bossra
            self.boss.hp = int(self.boss.hp * self.enemy_health_multiplier)
            self.boss.max_hp = int(self.boss.max_hp * self.enemy_health_multiplier)
            self.boss.attack_damage = int(
                self.boss.attack_damage * self.boss_damage_multiplier
            )
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

        # Ellenségeket szűrjük és jutalmazunk a halottakért
        alive_enemies = []
        for e in self.ellensegek:
            # Ha az ellenség halott és még nem kaptunk jutalmat
            if e.hp <= 0 and not getattr(e, "reward_given", False):
                reward = e.get_reward()
                self.penz += reward
                e.reward_given = True
                print(
                    f"+{reward} pénz ({e.__class__.__name__}lől) - Összesen: {self.penz}"
                )
            # Megtartjuk az élő ellenségeket és azokat, akik már átértek a végig
            if e.hp > 0 and not getattr(e, "reached_end", False):
                alive_enemies.append(e)

        self.ellensegek = alive_enemies

        # Ha a boss legyőzött, reseteljük a referenciát
        if self.boss is not None and self.boss not in self.ellensegek:
            self.boss = None

        # Halott tornyok eltávolítása
        for torony in list(self.palya.tornyok):
            if torony.hp <= 0:
                self.palya.remove_tower(torony)

        # Hullám vége ellenőrzés
        if self.maradek_ellenseg == 0 and len(self.ellensegek) == 0:
            self.hullam_fut = False

        # Auto wave mód: automatikusan szalad a következő wave-re
        if (
            self.continuous_waves
            and not self.hullam_fut
            and self.boss is None
            and len(self.ellensegek) == 0
            and self.maradek_ellenseg == 0
        ):
            if pygame.time.get_ticks() >= self.next_wave_auto_time:
                next_wave = self.hullam_szam + 1
                if next_wave <= 25:  # Max 25 wave
                    self.select_wave(next_wave)
                    self.next_wave_auto_time = (
                        pygame.time.get_ticks() + 500
                    )  # 0.5s delay
                else:
                    self.continuous_waves = False  # Vége

    def _draw_wave_select_menu(self) -> None:
        """Rajzol egy wave selection menüt."""
        # Háttér overlay
        overlay = pygame.Surface((SZELESSEG, MAGASSAG), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.ablak.blit(overlay, (0, 0))

        # Menü panel háttér
        panel_w, panel_h = 900, 550
        panel_x = (SZELESSEG - panel_w) // 2
        panel_y = (MAGASSAG - panel_h) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        pygame.draw.rect(self.ablak, (20, 20, 40), panel_rect)
        pygame.draw.rect(self.ablak, (100, 150, 255), panel_rect, 3, border_radius=10)

        # Cím
        title_font = pygame.font.SysFont("Arial", 32, bold=True)
        title = title_font.render("HULLÁM KIVÁLASZTÁSA", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SZELESSEG // 2, panel_y + 25))
        self.ablak.blit(title, title_rect)

        # 5 szint, mindegyik 5 wave gomb-mal
        small_font = pygame.font.SysFont("Arial", 14, bold=True)
        button_w, button_h = 70, 40
        spacing_x, spacing_y = 90, 80
        start_x = panel_x + 50
        start_y = panel_y + 70

        self.wave_button_rects = []

        for level in range(1, 6):
            # Szint címsor
            level_text = small_font.render(f"Szint {level}", True, (200, 255, 100))
            self.ablak.blit(
                level_text, (start_x - 10, start_y + (level - 1) * spacing_y - 25)
            )

            for wave_in_level in range(1, 6):
                wave_num = (level - 1) * 5 + wave_in_level
                x = start_x + (wave_in_level - 1) * spacing_x
                y = start_y + (level - 1) * spacing_y

                # Boss wave zöld, normál sárga
                is_boss = wave_num % 5 == 0
                btn_color = (50, 200, 50) if is_boss else (200, 200, 50)
                text_color = (255, 255, 255)

                # Gomb rajzolása
                btn_rect = pygame.Rect(x, y, button_w, button_h)
                pygame.draw.rect(self.ablak, btn_color, btn_rect)
                pygame.draw.rect(self.ablak, (255, 255, 255), btn_rect, 2)

                # Wave szám szövege
                btn_text = "Boss" if is_boss else f"W{wave_num}"
                wave_text = small_font.render(btn_text, True, text_color)
                wave_text_rect = wave_text.get_rect(center=btn_rect.center)
                self.ablak.blit(wave_text, wave_text_rect)

                # Hover effekt
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.ablak, (255, 255, 100), btn_rect, 3)

                self.wave_button_rects.append((btn_rect, wave_num))

        # Bezárás gomb
        close_btn_rect = pygame.Rect(panel_x + panel_w - 60, panel_y + 10, 50, 35)
        pygame.draw.rect(self.ablak, (200, 50, 50), close_btn_rect)
        pygame.draw.rect(self.ablak, (255, 255, 255), close_btn_rect, 2)
        close_text = small_font.render("X", True, (255, 255, 255))
        self.ablak.blit(
            close_text, (close_btn_rect.centerx - 7, close_btn_rect.centery - 7)
        )

        if close_btn_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.ablak, (255, 100, 100), close_btn_rect, 3)

        self.wave_close_rect = close_btn_rect

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

        # HUD panel a bal felső sarokban (külön háttérrel a tiszta megjelenítésért)
        hud_w, hud_h = 250, 110
        hud_bg = pygame.Surface((hud_w, hud_h), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 180))
        self.ablak.blit(hud_bg, (8, 8))
        pygame.draw.rect(
            self.ablak, (255, 255, 255), (8, 8, hud_w, hud_h), 2, border_radius=8
        )

        penz_surf = self.font.render(f"Pénz: {self.penz}", True, (255, 255, 255))
        self.ablak.blit(penz_surf, (20, 16))
        elet_szin = (255, 255, 255) if self.eletek > 1 else (255, 50, 50)
        elet_surf = self.font.render(f"Életek: {max(0, self.eletek)}", True, elet_szin)
        self.ablak.blit(elet_surf, (20, 44))

        if self.boss is not None:
            wave_status = f"Boss hullám: {self.hullam_szam}"
            hullam_active = False
        elif self.boss_pending:
            wave_status = "Boss készül..."
            hullam_active = False
        elif self.hullam_fut:
            wave_status = f"Hullám {self.hullam_szam} folyamatban"
            hullam_active = False
        else:
            wave_status = f"Következő hullám: {self.hullam_szam + 1}"
            hullam_active = True

        wave_surf = self.font.render(wave_status, True, (200, 200, 255))
        self.ablak.blit(wave_surf, (20, 72))

        # Auto wave mód status
        if self.continuous_waves:
            auto_status = "Auto: BE ▶"
            auto_surf = self.font.render(auto_status, True, (100, 255, 100))
            self.ablak.blit(auto_surf, (20, 100))

        # Gombok feliratai fix rövid formában (nem csúsznak szét): hullám indítás + mód kapcsoló
        self.hullam_gomb.draw(self.ablak, "Hullám váltása", hullam_active)

        # Wave indítása (auto mode) gomb
        wave_inditas_text = "Wave: BE ▶" if self.continuous_waves else "Wave indítása"
        wave_inditas_active = not self.hullam_fut and self.boss is None
        self.wave_inditas_gomb.draw(self.ablak, wave_inditas_text, wave_inditas_active)

        tornya_szoveg = "Tornyok: BE" if self.tornya_mod else "Tornyok: KI"
        self.tornya_gomb.draw(self.ablak, tornya_szoveg, True)

        fejlesztes_szoveg = "Fejl.: BE" if self.fejlesztes_mod else "Fejl.: KI"
        self.fejlesztes_gomb.draw(self.ablak, fejlesztes_szoveg, True)

        self.menu_gomb.draw(self.ablak, "Menü", True)

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

            # Fejlesztés panel háttér
            panel_w, panel_h = 420, 260
            panel_rect = pygame.Rect(
                (SZELESSEG - panel_w) // 2,
                (MAGASSAG - panel_h) // 2,
                panel_w,
                panel_h,
            )
            pygame.draw.rect(self.ablak, (20, 20, 30, 220), panel_rect)
            pygame.draw.rect(
                self.ablak, (200, 200, 255), panel_rect, 2, border_radius=10
            )

            # Torony információk
            tower = self.selected_upgrade_tower
            title = self.font.render(
                f"{tower.nev} - Level {tower.level}/{tower.max_level}",
                True,
                (255, 255, 255),
            )
            title_rect = title.get_rect(center=(SZELESSEG // 2, panel_rect.top + 40))
            self.ablak.blit(title, title_rect)

            # Jelenlegi statisztika
            stats_font = pygame.font.SysFont("Arial", 18)
            info_y = panel_rect.top + 80
            line_spacing = 28

            sebzes_text = stats_font.render(
                f"Sebzés: {tower.sebzes}", True, (255, 200, 0)
            )
            hatotav_text = stats_font.render(
                f"Hatótáv: {tower.hatotav:.1f}", True, (255, 200, 0)
            )
            speed_text = stats_font.render(
                f"Lövési sebesség: {tower.tuzelesi_sebesseg}ms", True, (255, 200, 0)
            )

            self.ablak.blit(sebzes_text, (panel_rect.left + 30, info_y))
            self.ablak.blit(hatotav_text, (panel_rect.left + 30, info_y + line_spacing))
            self.ablak.blit(
                speed_text, (panel_rect.left + 30, info_y + 2 * line_spacing)
            )

            # Fejlesztés költsége
            upgrade_cost = tower.get_upgrade_cost()
            if upgrade_cost > 0:
                cost_text = self.font.render(
                    f"Fejlesztés költsége: {upgrade_cost} pénz", True, (255, 100, 100)
                )
            else:
                cost_text = self.font.render(
                    "Maximum szint elérve!", True, (100, 255, 100)
                )

            cost_rect = cost_text.get_rect(
                center=(SZELESSEG // 2, panel_rect.top + 190)
            )
            self.ablak.blit(cost_text, cost_rect)

            # Gombok
            self.upgrade_button.rect.x = SZELESSEG // 2 - 90
            self.upgrade_button.rect.y = panel_rect.top + 210
            self.deselect_button.rect.x = SZELESSEG // 2 - 90
            self.deselect_button.rect.y = panel_rect.top + 248

            if upgrade_cost > 0:
                self.upgrade_button.draw(self.ablak, "Fejlesztés", True)
            else:
                self.upgrade_button.draw(self.ablak, "Nincs", False)

            self.deselect_button.draw(self.ablak, "Vissza", True)

        # Wave select menü rajzolása
        if self.wave_select_active:
            self._draw_wave_select_menu()

        pygame.display.update()

    def run(self) -> None:
        while self.futo:
            self.esemenyek()
            self.update()
            self.rajzol()
            self.ora.tick(60)
