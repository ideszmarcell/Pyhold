import pygame
import os
from settings import SZELESSEG, MAGASSAG
from button import Button


class StartScreen:
    def __init__(self) -> None:
        self.active = True
        self.font_title = pygame.font.SysFont("Georgia", 90, bold=True)
        self.font_logo = pygame.font.SysFont("Arial", 24, italic=True)

        # Lovagi arany és sötét kő színek
        self.lovagi_arany = (212, 175, 55)
        self.sotet_ko = (35, 40, 45)

        # Kép betöltése az "assets/images" mappából
        self.logo_img = None

        # --- ITT A FRISSÍTETT ELÉRÉSI ÚT ---
        kep_utvonal = os.path.join("assets", "images", "pyhold_borító.png")

        if os.path.exists(kep_utvonal):
            try:
                # Kép betöltése és átméretezése, hogy szépen elférjen középen
                eredeti_kep = pygame.image.load(kep_utvonal).convert_alpha()
                self.logo_img = pygame.transform.scale(eredeti_kep, (450, 450))
            except Exception as e:
                print(f"Hiba a kép betöltésekor: {e}")
        else:
            print(f"Figyelem: A kép nem található ezen az útvonalon: {kep_utvonal}")

        # Gombok lejjebb tolva, hogy elférjen a nagy kép
        self.start_btn = Button(SZELESSEG // 2 - 125, MAGASSAG - 190, 250, 45)
        self.quit_btn = Button(SZELESSEG // 2 - 125, MAGASSAG - 130, 250, 45)
        self.mute_btn = Button(SZELESSEG // 2 - 125, MAGASSAG - 70, 250, 45)

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

    def draw(self, felulet: pygame.Surface) -> None:
        if not self.active:
            return

        # Lovagi stílusú sötét háttér (acél/kő szín)
        felulet.fill(self.sotet_ko)

        # Cím felirat: Pyhold - Arany színnel
        title_surf = self.font_title.render("Pyhold", True, self.lovagi_arany)
        # Árnyék a szövegnek a drámaibb hatásért
        shadow_surf = self.font_title.render("Pyhold", True, (10, 10, 15))
        title_rect = title_surf.get_rect(center=(SZELESSEG // 2, 90))

        felulet.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
        felulet.blit(title_surf, title_rect)

        # Borítókép kirajzolása arany kerettel
        if self.logo_img:
            logo_rect = self.logo_img.get_rect(
                center=(SZELESSEG // 2, MAGASSAG // 2 - 10)
            )
            # Arany keret a kép köré
            keret_rect = logo_rect.inflate(10, 10)
            pygame.draw.rect(felulet, self.lovagi_arany, keret_rect, border_radius=8)
            # Maga a kép
            felulet.blit(self.logo_img, logo_rect)
        else:
            # Ha valamiért nem tölt be a kép, egy placeholder doboz jelenik meg
            logo_rect = pygame.Rect(0, 0, 400, 400)
            logo_rect.center = (SZELESSEG // 2, MAGASSAG // 2 - 10)
            pygame.draw.rect(felulet, (50, 55, 60), logo_rect, border_radius=15)
            pygame.draw.rect(felulet, self.lovagi_arany, logo_rect, 4, border_radius=15)

            logo_text = self.font_logo.render(
                "Kép nem található", True, (200, 200, 200)
            )
            logo_text_rect = logo_text.get_rect(center=logo_rect.center)
            felulet.blit(logo_text, logo_text_rect)

        # Gombok kirajzolása
        self.start_btn.draw(felulet, "Játék indítása", True)
        self.quit_btn.draw(felulet, "Kilépés", True)
        mute_text = "Némítás" if not self.muted else "Hang bekapcsolása"
        self.mute_btn.draw(felulet, mute_text, True)
