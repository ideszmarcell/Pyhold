import pygame
from core.settings import WHITE, BLUE


class Button:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.font_size: int = 22
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", self.font_size, bold=True)
        self.is_hovered: bool = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:

            self.is_hovered = self.rect.collidepoint(event.pos)
            if event.button == 1 and self.is_hovered:
                return True
        return False

    def draw(self, surface: pygame.Surface, text: str, active: bool) -> None:

        if active:
            color = (0, 150, 255) if self.is_hovered else BLUE
        else:
            color = (120, 120, 160) if self.is_hovered else (90, 90, 130)

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)


        max_text_width = self.rect.width - 12
        font_size = 22
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        text_surf = font.render(text, True, WHITE)

        while text_surf.get_width() > max_text_width and font_size > 10:
            font_size -= 1
            font = pygame.font.SysFont("Arial", font_size, bold=True)
            text_surf = font.render(text, True, WHITE)

        if text_surf.get_width() > max_text_width:

            trimmed = text
            while (
                trimmed
                and font.render(trimmed + "...", True, WHITE).get_width()
                > max_text_width
            ):
                trimmed = trimmed[:-1]
            text_surf = font.render(trimmed + "...", True, WHITE)

        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
