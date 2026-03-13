import pygame
from settings import FEHER, KEK

class Button:
    def __init__(self, x: int, y: int, szelesseg: int, magassag: int, szoveg: str, szin: tuple = KEK) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, szelesseg, magassag)
        self.szoveg: str = szoveg
        self.alap_szin: tuple = szin
        
        # Kiszámoljuk a "hover" (lebegés) színt: minden RGB értéket megnövelünk egy kicsit, de max 255-ig
        self.hover_szin: tuple = (
            min(szin[0] + 40, 255), 
            min(szin[1] + 40, 255), 
            min(szin[2] + 40, 255)
        )
        self.jelenlegi_szin: tuple = self.alap_szin
        
        # Szöveg beállítása (Arial, 20-as méret, vastag)
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", 20, bold=True)
        self.szoveg_kep: pygame.Surface = self.font.render(self.szoveg, True, FEHER)
        
        # A szöveget pontosan a gomb közepére igazítjuk
        self.szoveg_rect: pygame.Rect = self.szoveg_kep.get_rect(center=self.rect.center)
        self.hovered: bool = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Kezeli az egéreseményeket. Visszatér True-val, ha a gombra kattintottak."""
        if event.type == pygame.MOUSEMOTION:
            # Ellenőrzi, hogy az egér a gombon van-e
            self.hovered = self.rect.collidepoint(event.pos)
            self.jelenlegi_szin = self.hover_szin if self.hovered else self.alap_szin
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                return True
        return False

    def draw(self, felulet: pygame.Surface) -> None:
        """Kirajzolja a gombot a képernyőre."""
        # Gomb hátterének kirajzolása lekerekített sarkokkal (border_radius=8)
        pygame.draw.rect(felulet, self.jelenlegi_szin, self.rect, border_radius=8)
        # Gomb keretének kirajzolása (FEHER színű, 2 pixel vastag)
        pygame.draw.rect(felulet, FEHER, self.rect, 2, border_radius=8)
        # Szöveg rárajzolása a gombra
        felulet.blit(self.szoveg_kep, self.szoveg_rect)