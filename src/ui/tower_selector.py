import pygame
from core.settings import TOWER_COST, GRID_SIZE, WHITE, BLACK, DARK_GRAY


class TowerSelector:
    """Torony képválasztó UI elem."""

    def __init__(
        self, tower_images: dict[str, str], screen_width: int, screen_height: int
    ):
        self.tower_images = tower_images
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.active: bool = False
        self.tower_gx: int | None = None
        self.tower_gy: int | None = None

        self.image_size = GRID_SIZE * 2
        self.spacing = 10
        self.padding = 20

        self.images: dict[str, pygame.Surface] = {}
        self.buttons: dict[str, pygame.Rect] = {}

        self.menu_height = self.image_size + self.padding * 2
        self.menu_y = (screen_height - self.menu_height) // 2

        total_width = (
            len(tower_images) * self.image_size
            + (len(tower_images) - 1) * self.spacing
            + self.padding * 2
        )
        self.menu_x = (screen_width - total_width) // 2

        self.load_images()

    def load_images(self) -> None:
        """Betölti a tower képeket."""
        for name, path in self.tower_images.items():
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (self.image_size, self.image_size))
                self.images[name] = img
            except Exception as e:
                print(f"Hiba a {path} betöltésekor: {e}")

        x = self.menu_x + self.padding
        y = self.menu_y + self.padding

        for name in self.tower_images.keys():
            self.buttons[name] = pygame.Rect(x, y, self.image_size, self.image_size)
            x += self.image_size + self.spacing

    def show(self, tx: int, ty: int) -> None:
        """Megnyitja a választót egy adott toronyhoz."""
        self.active = True
        self.tower_gx = tx
        self.tower_gy = ty

    def hide(self) -> None:
        """Bezárja a választót."""
        self.active = False


    def handle_click(self, pos: tuple[int, int]) -> str | None:
        """
        Kezeli az egér kattintást.
        Visszatér a kiválasztott kép nevével, vagy None-nal ha nincs semmit kijelölve.
        """
        if not self.active:
            return None

        x, y = pos

        for name, rect in self.buttons.items():
            if rect.collidepoint(x, y):
                selected = name
                self.hide()
                return selected

        menu_rect = pygame.Rect(
            self.menu_x - 10,
            self.menu_y - 10,
            (self.image_size + self.spacing) * len(self.tower_images)
            + self.padding * 2
            + 10,
            self.menu_height + 20,
        )

        if not menu_rect.collidepoint(x, y):
            self.hide()

        return None

    def draw(self, surface: pygame.Surface) -> None:
        """Kirajzolja a képválasztó UI-t."""
        if not self.active:
            return

        # Háttér panel
        total_width = (
            len(self.tower_images) * self.image_size
            + (len(self.tower_images) - 1) * self.spacing
            + self.padding * 2
        )
        panel_rect = pygame.Rect(
            self.menu_x - 10, self.menu_y - 10, total_width + 20, self.menu_height + 20
        )

        # Háttér (homályosított)
        pygame.draw.rect(surface, BLACK, panel_rect)
        pygame.draw.rect(surface, DARK_GRAY, panel_rect, 3)

        # Képek kirajzolása
        for name, rect in self.buttons.items():
            if name in self.images:
                img = self.images[name]
                surface.blit(img, rect)
                # Szegély a kép körül
                pygame.draw.rect(surface, WHITE, rect, 2)

                # Árkijelzés
                cost_text = f"{TOWER_COST}"
                font = pygame.font.SysFont("Arial", 18, bold=True)
                text_surf = font.render(cost_text, True, WHITE)
                text_rect = text_surf.get_rect(midtop=(rect.centerx, rect.bottom + 4))
                surface.blit(text_surf, text_rect)
