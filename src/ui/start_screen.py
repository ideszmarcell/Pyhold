import pygame
import os
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import Button


class StartScreen:
    def __init__(self) -> None:
        self.active = True
        self.font_title = pygame.font.SysFont("Georgia", 90, bold=True)
        self.font_logo = pygame.font.SysFont("Arial", 24, italic=True)


        self.knight_gold = (212, 175, 55)
        self.dark_stone = (35, 40, 45)


        self.logo_img = None


        image_path = os.path.join("assets", "images", "pyhold_borító.png")

        if os.path.exists(image_path):
            try:

                original_image = pygame.image.load(image_path).convert_alpha()
                self.logo_img = pygame.transform.scale(original_image, (450, 450))
            except Exception as e:
                print(f"Hiba a kép betöltésekor: {e}")
        else:
            print(f"Figyelem: A kép nem található ezen az útvonalon: {image_path}")


        self.start_btn = Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT - 190, 250, 45)
        self.quit_btn = Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT - 130, 250, 45)
        self.mute_btn = Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT - 70, 250, 45)

        self.muted = False

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if not self.active:
            return None

        if self.start_btn.handle_event(event):
            return "start"
        if self.quit_btn.handle_event(event):
            return "quit"
        if self.mute_btn.handle_event(event):
            return "mute"

        return None

    def draw(self, surface: pygame.Surface) -> None:
        if not self.active:
            return


        surface.fill(self.dark_stone)


        title_surf = self.font_title.render("Pyhold", True, self.knight_gold)

        shadow_surf = self.font_title.render("Pyhold", True, (10, 10, 15))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 90))

        surface.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
        surface.blit(title_surf, title_rect)


        if self.logo_img:
            logo_rect = self.logo_img.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10)
            )

            border_rect = logo_rect.inflate(10, 10)
            pygame.draw.rect(surface, self.knight_gold, border_rect, border_radius=8)

            surface.blit(self.logo_img, logo_rect)
        else:

            logo_rect = pygame.Rect(0, 0, 400, 400)
            logo_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10)
            pygame.draw.rect(surface, (50, 55, 60), logo_rect, border_radius=15)
            pygame.draw.rect(surface, self.knight_gold, logo_rect, 4, border_radius=15)

            logo_text = self.font_logo.render(
                "Image not found", True, (200, 200, 200)
            )
            logo_text_rect = logo_text.get_rect(center=logo_rect.center)
            surface.blit(logo_text, logo_text_rect)


        self.start_btn.draw(surface, "Start Game", True)
        self.quit_btn.draw(surface, "Quit", True)
        mute_text = "Mute" if not self.muted else "Unmute"
        self.mute_btn.draw(surface, mute_text, True)
