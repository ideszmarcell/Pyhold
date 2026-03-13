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
            if event.button == 1 and self.is_hovered:
                return True
        return False

    def draw(self, felulet, szoveg, aktiv):
        # Ha nem aktív (fut a wave), akkor szürke, egyébként kék/világoskék
        szin = KEK if aktiv and not self.is_hovered else (0, 150, 255) if aktiv else (60, 60, 70)
        
        pygame.draw.rect(felulet, szin, self.rect, border_radius=10)
        pygame.draw.rect(felulet, FEHER, self.rect, 2, border_radius=10)

        text_surf = self.font.render(szoveg, True, FEHER)
        text_rect = text_surf.get_rect(center=self.rect.center)
        felulet.blit(text_surf, text_rect)