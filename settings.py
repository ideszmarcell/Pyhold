import sys
from typing import Tuple
import pygame

# pylint: disable=no-member

SZELESSEG, MAGASSAG = 800, 700
RACS_MERET = 40
FEKETE = (20, 20, 25)
SZURKE = (40, 40, 50)
ZOLD = (34, 139, 34)


class Palya:
    def __init__(self) -> None:
        self.oszlopok: int = SZELESSEG // RACS_MERET
        self.sorok: int = MAGASSAG // RACS_MERET
        self.adatok: list[list[int]] = [
            [0 for _ in range(self.oszlopok)] for _ in range(self.sorok)
        ]

    def koordinata_szamitas(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = pos
        return x // RACS_MERET, y // RACS_MERET

    def cella_modositas(self, pos: Tuple[int, int]) -> None:
        gx, gy = self.koordinata_szamitas(pos)
        if 0 <= gy < self.sorok and 0 <= gx < self.oszlopok:
            self.adatok[gy][gx] = 1 if self.adatok[gy][gx] == 0 else 0

    def _rajzol_vonalak(self, felulet: pygame.Surface) -> None:
        for x in range(0, SZELESSEG + 1, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (x, 0), (x, MAGASSAG))
        for y in range(0, MAGASSAG + 1, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (0, y), (SZELESSEG, y))

    def _rajzol_epuletek(self, felulet: pygame.Surface) -> None:
        for r in range(self.sorok):
            for c in range(self.oszlopok):
                if self.adatok[r][c] == 1:
                    rect = (
                        c * RACS_MERET + 2,
                        r * RACS_MERET + 2,
                        RACS_MERET - 4,
                        RACS_MERET - 4,
                    )
                    pygame.draw.rect(felulet, ZOLD, rect)

    def rajzol(self, felulet: pygame.Surface) -> None:
        felulet.fill(FEKETE)
        self._rajzol_epuletek(felulet)
        self._rajzol_vonalak(felulet)
