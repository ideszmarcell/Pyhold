import pygame
from settings import (
    KEK,
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

    def koordinata_szamitas(self, pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        return x // RACS_MERET, y // RACS_MERET

    def cella_modositas(self, pos: tuple[int, int]) -> None:
        gx, gy = self.koordinata_szamitas(pos)
        if 0 <= gy < self.sorok and 0 <= gx < self.oszlopok:
            self.adatok[gy][gx] = 1 if self.adatok[gy][gx] == 0 else 0

    def afectar_tornya_blokk(self, pos: tuple[int, int]) -> bool:
        """Hatást gyakorol az összes összekapcsolt tornyra a 2x2 blokkban. Visszatér True-val ha sikerült."""
        gx, gy = self.koordinata_szamitas(pos)
        
        # Ellenőrizd, hogy ez a cella torony-e
        if not (0 <= gy < self.sorok and 0 <= gx < self.oszlopok) or self.adatok[gy][gx] != 2:
            return False
        
        # Keresz meg a 2x2 blokk bal felső sarkát
        top_r, top_c = gy, gx
        
        # Ellenőrizd, ha ez nem a bal felső sarok
        if gy > 0 and gx > 0 and self.adatok[gy - 1][gx - 1] == 2:
            top_r, top_c = gy - 1, gx - 1
        elif gy > 0 and gx + 1 < self.oszlopok and self.adatok[gy - 1][gx] == 2:
            top_r, top_c = gy - 1, gx
        elif gx > 0 and gy + 1 < self.sorok and self.adatok[gy][gx - 1] == 2:
            top_r, top_c = gy, gx - 1
        
        # Hatást gyakorol az összes cellára a 2x2 blokkban
        for dr in range(2):
            for dc in range(2):
                nr, nc = top_r + dr, top_c + dc
                if 0 <= nr < self.sorok and 0 <= nc < self.oszlopok and self.adatok[nr][nc] == 2:
                    self.adatok[nr][nc] = 0  # Torony eltávolítása
        
        return True

    def _rajzol_vonalak(self, felulet: pygame.Surface) -> None:
        for x in range(0, self.oszlopok * RACS_MERET + 1, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (x, 0), (x, self.sorok * RACS_MERET))
        for y in range(0, self.sorok * RACS_MERET + 1, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (0, y), (self.oszlopok * RACS_MERET, y))

    def _rajzol_epuletek(self, felulet: pygame.Surface) -> None:
        rajzolt_tornyok: set[tuple[int, int]] = set()

        for r in range(self.sorok):
            for c in range(self.oszlopok):
                # Ha már rajzoltuk ezt a tornyot (2x2 blokkként), akkor kihagyjuk
                if (r, c) in rajzolt_tornyok:
                    continue

                szin = None
                szelesseg = RACS_MERET
                magassag = RACS_MERET

                if self.adatok[r][c] == 1:  # Fal
                    szin = FEKETE
                elif self.adatok[r][c] == 2:  # Torony
                    szin = ZOLD
                    # Ellenőrizd, hogy 2x2 blokkot alkot-e
                    if (
                        r + 1 < self.sorok
                        and c + 1 < self.oszlopok
                        and self.adatok[r][c + 1] == 2
                        and self.adatok[r + 1][c] == 2
                        and self.adatok[r + 1][c + 1] == 2
                    ):
                        szelesseg = RACS_MERET * 2
                        magassag = RACS_MERET * 2
                        # Jelöld fel az összes cellát mint rajzolt
                        rajzolt_tornyok.add((r, c))
                        rajzolt_tornyok.add((r, c + 1))
                        rajzolt_tornyok.add((r + 1, c))
                        rajzolt_tornyok.add((r + 1, c + 1))
                elif self.adatok[r][c] == 3:  # Speciális épület
                    szin = KEK
                elif self.adatok[r][c] == 6:  # Kezdőpont
                    szin = FEHER
                elif self.adatok[r][c] == 5:  # Végpont (Bázis)
                    szin = (255, 50, 50)
                else:
                    # BIZTONSÁGI HÁLÓ: Ha ismeretlen szám van a pályán, legyen rikító lila!
                    szin = (255, 0, 255)

                # Rajzolás
                rect = pygame.Rect(c * RACS_MERET, r * RACS_MERET, szelesseg, magassag)
                pygame.draw.rect(felulet, szin, rect)

                rect = (
                    c * RACS_MERET + 1,
                    r * RACS_MERET + 1,
                    szelesseg - 2,
                    magassag - 2,
                )
                pygame.draw.rect(felulet, szin, rect)

    def rajzol(self, felulet: pygame.Surface) -> None:
        felulet.fill(FEKETE)
        self._rajzol_epuletek(felulet)
        self._rajzol_vonalak(felulet)

    def kinyer_utvonal(self) -> list[tuple[int, int]]:
        """Kikeresi a pixel-alapú útvonalat a 6-ostól az 5-ösig, figyelve a kereszteződésekre."""
        start: tuple[int, int] | None = None
        end: tuple[int, int] | None = None

        for r in range(self.sorok):
            for c in range(self.oszlopok):
                if self.adatok[r][c] == 6:
                    start = (r, c)
                elif self.adatok[r][c] == 5:
                    end = (r, c)

        if not start or not end:
            return []

        utvonal_rida: list[tuple[int, int]] = [start]
        jelenlegi: tuple[int, int] = start
        iranyok: list[tuple[int, int]] = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]  # Fel, Le, Balra, Jobbra
        jelenlegi_irany = None

        for dr, dc in iranyok:
            nr, nc = start[0] + dr, start[1] + dc
            if 0 <= nr < self.sorok and 0 <= nc < self.oszlopok:
                if self.adatok[nr][nc] in [0, 5]:
                    jelenlegi_irany = (dr, dc)
                    break

        if not jelenlegi_irany:
            return []

        biztonsagi_fek = 0
        while jelenlegi != end and biztonsagi_fek < 1000:
            biztonsagi_fek += 1
            dr, dc = jelenlegi_irany
            elore_r, elore_c = jelenlegi[0] + dr, jelenlegi[1] + dc

            if (
                0 <= elore_r < self.sorok
                and 0 <= elore_c < self.oszlopok
                and self.adatok[elore_r][elore_c] in [0, 5]
            ):
                jelenlegi = (elore_r, elore_c)
                utvonal_rida.append(jelenlegi)
            else:
                talalt = False
                for uj_dr, uj_dc in iranyok:
                    if uj_dr == -dr and uj_dc == -dc:
                        continue

                    nr, nc = jelenlegi[0] + uj_dr, jelenlegi[1] + uj_dc
                    if 0 <= nr < self.sorok and 0 <= nc < self.oszlopok:
                        if self.adatok[nr][nc] in [0, 5]:
                            jelenlegi_irany = (uj_dr, uj_dc)
                            jelenlegi = (nr, nc)
                            utvonal_rida.append(jelenlegi)
                            talalt = True
                            break

                if not talalt:
                    break

        # Rács koordináták konvertálása pixel koordinátákká (a cella közepe)
        pixel_utvonal: list[tuple[int, int]] = []
        for r, c in utvonal_rida:
            px = c * RACS_MERET + (RACS_MERET // 2)
            py = r * RACS_MERET + (RACS_MERET // 2)
            pixel_utvonal.append((px, py))

        return pixel_utvonal
