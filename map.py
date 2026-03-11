from typing import Tuple
import pygame
from settings import (
    RACS_MERET,
    FEKETE,
    SZURKE,
    ZOLD,
    FEHER,
    MAZE,
)

# pylint: disable=no-member


class Palya:
    def __init__(self) -> None:
        self.oszlopok: int = len(MAZE[0])
        self.sorok: int = len(MAZE)
        self.adatok: list[list[int]] = [row[:] for row in MAZE]

    def koordinata_szamitas(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = pos
        return x // RACS_MERET, y // RACS_MERET

    def cella_modositas(self, pos: Tuple[int, int]) -> None:
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
                elif self.adatok[r][c] == 0:  # Üres / út (kék)
                    szin = FEHER
                elif self.adatok[r][c] == 2:  # Torony (zöld)
                    szin = ZOLD

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
