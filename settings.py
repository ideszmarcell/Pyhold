import pygame

# pylint: disable=no-member

SZELESSEG, MAGASSAG = 800, 500
RACS_MERET = 40
FEKETE = (20, 20, 25)
SZURKE = (40, 40, 50)
ZOLD = (34, 139, 34)
FEHER = (255, 255, 255)
KEK = (0, 102, 204)


MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Palya:
    def __init__(self) -> None:
        self.oszlopok: int = len(MAZE[0])
        self.sorok: int = len(MAZE)
        self.adatok: list[list[int]] = [row[:] for row in MAZE]

    def koordinata_szamitas(self, pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        return x // RACS_MERET, y // RACS_MERET

    def cella_modositas(self, pos: tuple[int, int]) -> None:
        gx, gy = self.koordinata_szamitas(pos)
        if 0 <= gy < self.sorok and 0 <= gx < self.oszlopok:
            self.adatok[gy][gx] = 1 if self.adatok[gy][gx] == 0 else 0

    def _rajzol_vonalak(self, felulet: pygame.Surface) -> None:
        for x in range(0, self.oszlopok * RACS_MERET + 1, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (x, 0), (x, self.sorok * RACS_MERET))
        for y in range(0, self.sorok * RACS_MERET + 1, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (0, y), (self.oszlopok * RACS_MERET, y))

    def _rajzol_epuletek(self, felulet: pygame.Surface) -> None:
        for r in range(self.sorok):
            for c in range(self.oszlopok):
                szin = None
                if self.adatok[r][c] == 1:  # Fal
                    szin = FEKETE
                else:  # Üres / út (kék)
                    szin = FEHER

                rect = (
                    c * RACS_MERET + 1,
                    r * RACS_MERET + 1,
                    RACS_MERET - 2,
                    RACS_MERET - 2,
                )
                pygame.draw.rect(felulet, szin, rect)

    def rajzol(self, felulet: pygame.Surface) -> None:
        felulet.fill(FEKETE)
        self._rajzol_epuletek(felulet)
        self._rajzol_vonalak(felulet)
