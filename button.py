import pygame
from settings import FEHER, KEK, SZURKE

class Button:
    def __init__(self, x, y, szelesseg, magassag):
        self.rect = pygame.Rect(x, y, szelesseg, magassag)
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Frissítsük az is_hovered flag-et az egér aktuális pozíciója alapján
            self.is_hovered = self.rect.collidepoint(event.pos)
            if event.button == 1 and self.is_hovered:
                return True
        return False

    def draw(self, felulet, szoveg, aktiv):
        # Ha nem aktív (fut a wave), akkor szürke, egyébként kék/világoskék
        szin = KEK if aktiv and not self.is_hovered else (0, 150, 255) if aktiv else (60, 60, 70)
        
        pygame.draw.rect(felulet, szin, self.rect, border_radius=10)
        pygame.draw.rect(felulet, FEHER, self.rect, 2, border_radius=10)

        # Automatikus betűméretezés/kivágás, hogy szöveg ne tolódjon ki a gombból
        max_text_width = self.rect.width - 12
        font_size = 22
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        text_surf = font.render(szoveg, True, FEHER)

        while text_surf.get_width() > max_text_width and font_size > 10:
            font_size -= 1
            font = pygame.font.SysFont("Arial", font_size, bold=True)
            text_surf = font.render(szoveg, True, FEHER)

        if text_surf.get_width() > max_text_width:
            # Vágjuk a szöveget: végén pontozottság, hogy beleférjen
            trimmed = szoveg
            while trimmed and font.render(trimmed + "...", True, FEHER).get_width() > max_text_width:
                trimmed = trimmed[:-1]
            text_surf = font.render(trimmed + "...", True, FEHER)

        text_rect = text_surf.get_rect(center=self.rect.center)
        felulet.blit(text_surf, text_rect)