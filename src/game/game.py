import pygame
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TOWER_COST
from game.map import Map
from entities.basic_enemy import BasicEnemy
from entities.tank_enemy import TankEnemy
from entities.fast_enemy import FastEnemy
from entities.armored_enemy import ArmoredEnemy
from entities.boss_enemy import BossEnemy
from entities.enemy import Enemy
from entities.tower import Tower
from ui.tower_selector import TowerSelector
from game.game_over import GameOverScreen
from ui.start_screen import StartScreen
from managers.economy_manager import EconomyManager
from managers.wave_manager import WaveManager
from managers.game_state import GameStateManager, GameMode
from managers.ui_manager import UIManager


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/pyhold_muzsika.mp3")
        pygame.mixer.music.play(-1)
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = Map()
        self.economy = EconomyManager(starting_money=250)
        self.state = GameStateManager()
        self.wave_manager = WaveManager()
        Tower.load_images()
        self.tower_selector = TowerSelector(Tower.TOWER_IMAGES, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.ui = UIManager()

        self.running: bool = True
        self.path: list[tuple[int, int]] = self.map.extract_path()
        self.enemies: list[Enemy] = []
        self.last_spawn_time: int = 0
        self.selected_upgrade_tower: Tower | None = None
        self.boss: BossEnemy | None = None
        self.boss_spawned_wave: int = 0
        self.boss_pending: bool = False
        self.boss_spawn_delay_ms: int = 2000
        self.boss_spawn_ready_time: int = 0
        self.boss_reward: int = 175
        self.boss_defeated_wave: int = 0
        self.wave_select_active: bool = False
        self.wave_button_rects: list[tuple[pygame.Rect, int]] = []
        self.wave_close_rect: pygame.Rect | None = None
        self.continuous_waves: bool = False
        self.next_wave_auto_time: int = 0

        self.font = pygame.font.SysFont("Arial", 22, bold=True)

        self.muted = False

        self.game_over_screen = GameOverScreen()
        self.start_screen = StartScreen()

    def start_wave_selection(self):
        """Megnyitja a wave select menüt."""
        if self.boss is not None or self.wave_manager.is_running:
            return
        self.wave_select_active = True

    def select_wave(self, wave_number: int) -> None:
        """Kiválasztott wave-t indítja el."""
        if self.boss is not None or self.wave_manager.is_running or len(self.enemies) > 0:
            return

        self.wave_select_active = False
        self.wave_manager.start_wave(wave_number)
        level = (wave_number - 1) // 5 + 1
        health_mult, count_mult, boss_dmg_mult = self.wave_manager.get_scaling_info()
        print(
            f"Wave {wave_number} (Level {level}) scaling: HP: {health_mult:.2f}x, Count: {count_mult:.2f}x, Boss DMG: {boss_dmg_mult:.2f}x"
        )

    def start_continuous_waves(self, starting_wave: int = 1) -> None:
        """Auto wave mód bekapcsolása a megadott wave-től."""
        if self.continuous_waves:
            return
        self.continuous_waves = True
        self.wave_manager.current_wave = starting_wave - 1
        self.next_wave_auto_time = pygame.time.get_ticks() + 1000

    def stop_continuous_waves(self) -> None:
        """Auto wave mód kikapcsolása."""
        self.continuous_waves = False
        self.next_wave_auto_time = 0

    def _click_on_ui_buttons(self, pos: tuple[int, int]) -> bool:
        return (
            self.ui.select_wave_btn.rect.collidepoint(pos)
            or self.ui.start_wave_btn.rect.collidepoint(pos)
            or self.ui.towers_btn.rect.collidepoint(pos)
            or self.ui.upgrade_btn.rect.collidepoint(pos)
            or self.ui.menu_btn.rect.collidepoint(pos)
        )

    def toggle_mute(self) -> None:
        if self.muted:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.muted = not self.muted

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.start_screen.active:
                action = self.start_screen.handle_event(event)
                if action == "start":
                    self.start_screen.active = False
                elif action == "quit":
                    self.running = False
                elif action == "mute":
                    self.toggle_mute()
                    self.start_screen.muted = self.muted
                continue

            if self.state.tower_upgrade_mode and self.selected_upgrade_tower:
                self.ui.upgrade_confirm_btn.handle_event(event)
                self.ui.upgrade_cancel_btn.handle_event(event)

            if self.game_over_screen.active:
                action = self.game_over_screen.handle_event(event)
                if action == "restart":
                    self.__init__()
                elif action == "quit":
                    self.running = False
                continue

            if self.ui.menu_btn.handle_event(event):
                self.state.toggle_menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.wave_select_active = False
                self.state.toggle_menu()
                self.selected_upgrade_tower = None
                self.state.tower_upgrade_mode = False

            if self.state.menu_mode:
                if self.ui.resume_btn.handle_event(event):
                    self.state.toggle_menu()
                if self.ui.quit_btn.handle_event(event):
                    self.running = False
                if self.ui.mute_btn.handle_event(event):
                    self.toggle_mute()
                continue

            if self.ui.select_wave_btn.handle_event(event):
                self.start_wave_selection()

            if self.ui.start_wave_btn.handle_event(event):
                if not self.continuous_waves:
                    self.start_continuous_waves(1)
                else:
                    self.stop_continuous_waves()

            if self.ui.towers_btn.handle_event(event):
                self.state.tower_building_mode = not self.state.tower_building_mode
                if not self.state.tower_building_mode:
                    self.tower_selector.hide()

            if self.ui.upgrade_btn.handle_event(event):
                self.state.tower_upgrade_mode = (
                    not self.state.tower_upgrade_mode
                )
                if not self.state.tower_upgrade_mode:
                    self.selected_upgrade_tower = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos

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

                    if self._click_on_ui_buttons(mouse_pos):
                        continue

                    if self.state.tower_upgrade_mode and self.selected_upgrade_tower:
                        if self.ui.upgrade_cancel_btn.is_hovered:
                            self.selected_upgrade_tower = None
                            continue

                        if self.ui.upgrade_confirm_btn.is_hovered:
                            upgrade_cost = (
                                self.selected_upgrade_tower.get_upgrade_cost()
                            )
                            if upgrade_cost > 0:
                                if self.economy.can_afford(upgrade_cost):
                                    self.economy.spend(upgrade_cost, "Tower upgrade")
                                    self.selected_upgrade_tower.upgrade()
                                    print(
                                        f"Tower upgraded! Level: {self.selected_upgrade_tower.level}"
                                    )
                                else:
                                    print(
                                        f"Not enough money! Required: {upgrade_cost}, Have: {self.economy.get_balance()}"
                                    )
                            else:
                                print("Tower is already at max level!")
                            continue

                        continue

                    if self.tower_selector.active:
                        selected_image = self.tower_selector.handle_click(event.pos)
                        if selected_image:
                            cost = TOWER_COST
                            if self.economy.can_afford(cost):
                                self.economy.spend(cost, "Tower purchase")
                                if self.tower_selector.tower_gy is not None and self.tower_selector.tower_gx is not None:
                                    self.map.set_tower_image(
                                        self.tower_selector.tower_gy,
                                        self.tower_selector.tower_gx,
                                        selected_image,
                                    )
                                self.state.tower_building_mode = False
                            else:
                                print("Not enough money to buy tower!")

                    elif self.state.tower_building_mode and not self._click_on_ui_buttons(event.pos):
                        gx, gy = self.map.calculate_coords(event.pos)
                        if (
                            0 <= gy < self.map.rows
                            and 0 <= gx < self.map.cols
                            and self.map.data[gy][gx] == 2
                        ):
                            if self.map.get_tower_image(gy, gx) is None:
                                self.tower_selector.show(gx, gy)
                            else:
                                self.state.tower_building_mode = False
                    elif self.state.tower_upgrade_mode and not self._click_on_ui_buttons(
                        event.pos
                    ):
                        gx, gy = self.map.calculate_coords(event.pos)
                        if (
                            0 <= gy < self.map.rows
                            and 0 <= gx < self.map.cols
                            and self.map.data[gy][gx] == 2
                        ):
                            tower_at_pos = None
                            for tower in self.map.towers:
                                if (
                                    tower.gx <= gx < tower.gx + tower.size
                                    and tower.gy <= gy < tower.gy + tower.size
                                ):
                                    tower_at_pos = tower
                                    break

                            if tower_at_pos:
                                self.selected_upgrade_tower = tower_at_pos
                            else:
                                self.selected_upgrade_tower = None

    def update(self):
        if self.start_screen.active or self.state.menu_mode or self.game_over_screen.active:
            return

        if self.wave_manager.is_running and self.wave_manager.remaining_enemies > 0:
            most = pygame.time.get_ticks()
            if most - self.last_spawn_time > 800:
                if self.path:
                    from typing import Callable

                    enemy_types: list[Callable[[list[tuple[int, int]]], Enemy]] = [
                        BasicEnemy,
                        FastEnemy,
                        TankEnemy,
                        ArmoredEnemy,
                    ]
                    enemy_index: int = (self.wave_manager.remaining_enemies % 5) % len(enemy_types)
                    selected_enemy = enemy_types[enemy_index]

                    enemy: Enemy = selected_enemy(self.path)
                    health_mult, _, _ = self.wave_manager.get_scaling_info()
                    enemy.hp = int(enemy.hp * health_mult)
                    enemy.max_hp = int(enemy.max_hp * health_mult)
                    self.enemies.append(enemy)
                self.wave_manager.spawn_enemy()
                self.last_spawn_time = most

        for tower in self.map.towers:
            tower.find_target(self.enemies)

        is_boss_wave = self.wave_manager.current_wave > 0 and self.wave_manager.current_wave % 5 == 0

        if (
            is_boss_wave
            and not self.wave_manager.is_running
            and self.wave_manager.remaining_enemies == 0
            and len(self.enemies) == 0
            and self.wave_manager.current_wave > 0
            and self.boss_spawned_wave < self.wave_manager.current_wave
        ):
            if not self.boss_pending:
                self.economy.earn(100, "Boss incoming bonus")
                print(f"Before Boss: +100 money (total: {self.economy.get_balance()})")
                self.boss_pending = True
                self.boss_spawn_ready_time = (
                    pygame.time.get_ticks() + self.boss_spawn_delay_ms
                )

        if self.boss_pending and pygame.time.get_ticks() >= self.boss_spawn_ready_time:
            self.boss = BossEnemy(self.path, wave=self.wave_manager.current_wave)
            health_mult, _, boss_dmg_mult = self.wave_manager.get_scaling_info()
            self.boss.hp = int(self.boss.hp * health_mult)
            self.boss.max_hp = int(self.boss.max_hp * health_mult)
            self.boss.attack_damage = int(
                self.boss.attack_damage * boss_dmg_mult
            )
            self.enemies.append(self.boss)
            self.boss_spawned_wave = self.wave_manager.current_wave
            self.boss_pending = False

        for e in list(self.enemies):
            if isinstance(e, BossEnemy):
                e.update(self.map.towers)
            else:
                e.update()

        for e in self.enemies:
            if getattr(e, "reached_end", False):
                if isinstance(e, BossEnemy):
                    self.state.lives = 0
                    self.state.current_mode = GameMode.GAME_OVER
                    self.game_over_screen.active = True
                else:
                    if self.state.lose_life():
                        self.game_over_screen.active = True

        alive_enemies: list[Enemy] = []
        for e in self.enemies:
            if e.hp <= 0 and not getattr(e, "reward_given", False):
                reward = e.get_reward()
                self.economy.earn(reward, f"Enemy defeated ({e.__class__.__name__})")
                e.reward_given = True
                print(
                    f"+{reward} money ({e.__class__.__name__} from) - Total: {self.economy.get_balance()}"
                )
            if e.hp > 0 and not getattr(e, "reached_end", False):
                alive_enemies.append(e)

        self.enemies = alive_enemies

        if self.boss is not None and self.boss not in self.enemies:
            self.boss = None

        for tower in list(self.map.towers):
            if tower.hp <= 0:
                self.map.remove_tower(tower)

        if self.wave_manager.remaining_enemies == 0 and len(self.enemies) == 0:
            self.wave_manager.is_running = False

        if (
            self.continuous_waves
            and not self.wave_manager.is_running
            and self.boss is None
            and len(self.enemies) == 0
            and self.wave_manager.remaining_enemies == 0
        ):
            if pygame.time.get_ticks() >= self.next_wave_auto_time:
                next_wave = self.wave_manager.current_wave + 1
                if next_wave <= 25:
                    self.select_wave(next_wave)
                    self.next_wave_auto_time = (
                        pygame.time.get_ticks() + 500
                    )
                else:
                    self.continuous_waves = False

    def _draw_wave_select_menu(self) -> None:
        """Rajzol egy wave selection menüt."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.surface.blit(overlay, (0, 0))

        panel_w, panel_h = 750, 420
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        pygame.draw.rect(self.surface, (20, 20, 40), panel_rect)
        pygame.draw.rect(self.surface, (100, 150, 255), panel_rect, 3, border_radius=10)

        title_font = pygame.font.SysFont("Arial", 28, bold=True)
        title = title_font.render("WAVE SELECTION", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, panel_y + 20))
        self.surface.blit(title, title_rect)

        small_font = pygame.font.SysFont("Arial", 12, bold=True)
        button_w, button_h = 60, 35
        spacing_x, spacing_y = 75, 65
        start_x = panel_x + 40
        start_y = panel_y + 55

        self.wave_button_rects = []

        for level in range(1, 6):
            level_text = small_font.render(f"Level {level}", True, (200, 255, 100))
            self.surface.blit(
                level_text, (start_x - 10, start_y + (level - 1) * spacing_y - 25)
            )

            for wave_in_level in range(1, 6):
                wave_num = (level - 1) * 5 + wave_in_level
                x = start_x + (wave_in_level - 1) * spacing_x
                y = start_y + (level - 1) * spacing_y

                is_boss = wave_num % 5 == 0
                btn_color = (50, 200, 50) if is_boss else (200, 200, 50)
                text_color = (255, 255, 255)

                btn_rect = pygame.Rect(x, y, button_w, button_h)
                pygame.draw.rect(self.surface, btn_color, btn_rect)
                pygame.draw.rect(self.surface, (255, 255, 255), btn_rect, 2)

                btn_text = "Boss" if is_boss else f"W{wave_num}"
                wave_text = small_font.render(btn_text, True, text_color)
                wave_text_rect = wave_text.get_rect(center=btn_rect.center)
                self.surface.blit(wave_text, wave_text_rect)

                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.surface, (255, 255, 100), btn_rect, 3)

                self.wave_button_rects.append((btn_rect, wave_num))

        close_btn_rect = pygame.Rect(panel_x + panel_w - 55, panel_y + 8, 45, 30)
        pygame.draw.rect(self.surface, (200, 50, 50), close_btn_rect)
        pygame.draw.rect(self.surface, (255, 255, 255), close_btn_rect, 2)
        close_text = small_font.render("X", True, (255, 255, 255))
        self.surface.blit(
            close_text, (close_btn_rect.centerx - 6, close_btn_rect.centery - 6)
        )

        if close_btn_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.surface, (255, 100, 100), close_btn_rect, 3)

        self.wave_close_rect = close_btn_rect

    def draw(self) -> None:
        if self.start_screen.active:
            self.start_screen.draw(self.surface)
            pygame.display.update()
            return

        self.map.draw(self.surface)

        for tower in self.map.towers:
            tower.draw(self.surface, self.map.offset_x, self.map.offset_y)

        for e in self.enemies[:]:
            e.draw(self.surface, self.map.offset_x, self.map.offset_y)

        hud_w, hud_h = 320, 140
        hud_bg = pygame.Surface((hud_w, hud_h), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 180))
        self.surface.blit(hud_bg, (8, 8))
        pygame.draw.rect(
            self.surface, (255, 255, 255), (8, 8, hud_w, hud_h), 2, border_radius=8
        )

        money_surf = self.font.render(f"Money: {self.economy.get_balance()}", True, (255, 255, 255))
        self.surface.blit(money_surf, (20, 16))
        health_color = (255, 100, 100) if self.state.lives > 1 else (255, 50, 50)
        health_surf = self.font.render("♥" * max(0, self.state.lives), True, health_color)
        self.surface.blit(health_surf, (20, 44))

        wave_text = f"Wave: {self.wave_manager.current_wave}" if self.wave_manager.current_wave > 0 else "Wave: 0"
        wave_surf = self.font.render(wave_text, True, (255, 255, 255))
        self.surface.blit(wave_surf, (20, 72))

        auto_wave_text = "AUTO WAVE: ON" if self.continuous_waves else "AUTO WAVE: OFF"
        auto_wave_surf = self.font.render(auto_wave_text, True, (255, 255, 255))
        self.surface.blit(auto_wave_surf, (20, 98))

        if self.state.tower_upgrade_mode and self.selected_upgrade_tower:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.surface.blit(overlay, (0, 0))

            panel_w, panel_h = 420, 260
            panel_rect = pygame.Rect(
                (SCREEN_WIDTH - panel_w) // 2,
                (SCREEN_HEIGHT - panel_h) // 2,
                panel_w,
                panel_h,
            )
            pygame.draw.rect(self.surface, (20, 20, 30, 220), panel_rect)
            pygame.draw.rect(
                self.surface, (200, 200, 255), panel_rect, 2, border_radius=10
            )

            tower = self.selected_upgrade_tower
            title = self.font.render(
                f"{tower.name} - Level {tower.level}/{tower.max_level}",
                True,
                (255, 255, 255),
            )
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 40))
            self.surface.blit(title, title_rect)

            stats_font = pygame.font.SysFont("Arial", 18)
            info_y = panel_rect.top + 80
            line_spacing = 28

            sebzes_text = stats_font.render(
                f"Damage: {tower.damage}", True, (255, 200, 0)
            )
            hatotav_text = stats_font.render(
                f"Range: {tower.range:.1f}", True, (255, 200, 0)
            )
            speed_text = stats_font.render(
                f"Fire Speed: {tower.fire_speed}ms", True, (255, 200, 0)
            )

            self.surface.blit(sebzes_text, (panel_rect.left + 30, info_y))
            self.surface.blit(hatotav_text, (panel_rect.left + 30, info_y + line_spacing))
            self.surface.blit(
                speed_text, (panel_rect.left + 30, info_y + 2 * line_spacing)
            )

            upgrade_cost = tower.get_upgrade_cost()
            if upgrade_cost > 0:
                cost_text = self.font.render(
                    f"Upgrade Cost: {upgrade_cost} money", True, (255, 100, 100)
                )
            else:
                cost_text = self.font.render(
                    "Max level reached!", True, (100, 255, 100)
                )

            cost_rect = cost_text.get_rect(
                center=(SCREEN_WIDTH // 2, panel_rect.top + 190)
            )
            self.surface.blit(cost_text, cost_rect)

            self.ui.upgrade_confirm_btn.rect.x = SCREEN_WIDTH // 2 - 90
            self.ui.upgrade_confirm_btn.rect.y = panel_rect.top + 210
            self.ui.upgrade_cancel_btn.rect.x = SCREEN_WIDTH // 2 - 90
            self.ui.upgrade_cancel_btn.rect.y = panel_rect.top + 248

            if upgrade_cost > 0:
                self.ui.upgrade_confirm_btn.draw(self.surface, "Upgrade", True)
            else:
                self.ui.upgrade_confirm_btn.draw(self.surface, "Max Level", False)

            self.ui.upgrade_cancel_btn.draw(self.surface, "Back", True)

        if self.wave_select_active:
            self._draw_wave_select_menu()

        self.ui.select_wave_btn.draw(self.surface, "Select Wave", True)
        self.ui.start_wave_btn.draw(self.surface, "Start Wave", True)
        self.ui.towers_btn.draw(self.surface, "Build Tower", self.state.tower_building_mode)
        self.ui.upgrade_btn.draw(self.surface, "Upgrade Tower", self.state.tower_upgrade_mode)
        self.ui.menu_btn.draw(self.surface, "Menu", True)

        if self.state.tower_building_mode:
            self.tower_selector.draw(self.surface)

        if self.state.menu_mode:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.surface.blit(overlay, (0, 0))

            panel_w, panel_h = 300, 250
            panel_rect = pygame.Rect(
                (SCREEN_WIDTH - panel_w) // 2,
                (SCREEN_HEIGHT - panel_h) // 2,
                panel_w,
                panel_h,
            )
            pygame.draw.rect(self.surface, (20, 20, 30, 240), panel_rect)
            pygame.draw.rect(
                self.surface, (200, 200, 255), panel_rect, 2, border_radius=10
            )

            menu_title = self.font.render("MENU", True, (255, 255, 255))
            menu_title_rect = menu_title.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top + 30))
            self.surface.blit(menu_title, menu_title_rect)

            self.ui.resume_btn.rect.x = SCREEN_WIDTH // 2 - 90
            self.ui.resume_btn.rect.y = panel_rect.top + 80
            self.ui.mute_btn.rect.x = SCREEN_WIDTH // 2 - 90
            self.ui.mute_btn.rect.y = panel_rect.top + 130
            self.ui.quit_btn.rect.x = SCREEN_WIDTH // 2 - 90
            self.ui.quit_btn.rect.y = panel_rect.top + 180

            mute_text = "Unmute" if self.muted else "Mute"
            self.ui.resume_btn.draw(self.surface, "Resume", True)
            self.ui.mute_btn.draw(self.surface, mute_text, True)
            self.ui.quit_btn.draw(self.surface, "Quit", True)

        if self.game_over_screen.active:
            self.game_over_screen.draw(self.surface, self.wave_manager.current_wave)

        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
