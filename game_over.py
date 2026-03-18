import pygame
from settings import SZELESSEG, MAGASSAG
from button import Button

class GameOverScreen:
    def __init__(self) -> None:
        self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
        
        # Pontosan középre igazított gombok (x: középen, y: kicsit a szöveg alatt)
        self.restart_btn = Button(SZELESSEG // 2 - 90, MAGASSAG // 2 + 20, 180, 45)
        self.quit_btn = Button(SZELESSEG // 2 - 90, MAGASSAG // 2 + 80, 180, 45)
        self.active = False

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Kezeli a kattintást. Ha a restartra nyomnak, visszaszól a game.py-nak."""
        if not self.active:
            return None
        
        if self.restart_btn.handle_event(event):
            return "restart"
        if self.quit_btn.handle_event(event):
            return "quit"
        
        return None

    def draw(self, felulet: pygame.Surface, hullam_szam: int) -> None:
        """Kirajzolja a fekete hátteret, a szöveget és a gombot."""
        if not self.active:
            return

        # Sötétített, félig átlátszó háttér
        overlay = pygame.Surface((SZELESSEG, MAGASSAG), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        felulet.blit(overlay, (0, 0))

        # GAME OVER felirat
        title_surf = self.font_large.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_surf.get_rect(center=(SZELESSEG // 2, MAGASSAG // 2 - 60))
        felulet.blit(title_surf, title_rect)

        # Gombok kirajzolása
        self.restart_btn.draw(felulet, "Újraindítás", True)
        self.quit_btn.draw(felulet, "Kilépés", True)