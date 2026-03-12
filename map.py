
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
                elif self.adatok[r][c] == 2:  # Torony (zöld)
                    szin = ZOLD
                elif self.adatok[r][c] == 3:  # Speciális épület (kék)
                    szin = KEK
                elif self.adatok[r][c] == 6:  # ÚJ: Kezdőpont
                    szin = FEHER
                elif self.adatok[r][c] == 5:  # ÚJ: Végpont (Bázis) - legyen mondjuk piros
                    szin = (255, 50, 50)
                else:
                    # BIZTONSÁGI HÁLÓ: Ha ismeretlen szám van a pályán, legyen rikító lila!
                    szin = (255, 0, 255) 

                # Rajzolás
                rect = pygame.Rect(c * RACS_MERET, r * RACS_MERET, RACS_MERET, RACS_MERET)
                pygame.draw.rect(felulet, szin, rect)

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

    def kinyer_utvonal(self) -> list[tuple[int, int]]:
        """Kikeresi a pixel-alapú útvonalat a 6-ostól az 5-ösig, figyelve a kereszteződésekre."""
        start = None
        end = None
        
        # 1. Megkeressük a kezdő (6) és végpontot (5)
        for r in range(self.sorok):
            for c in range(self.oszlopok):
                if self.adatok[r][c] == 6:
                    start = (r, c)
                elif self.adatok[r][c] == 5:
                    end = (r, c)

        if not start or not end:
            return []

        utvonal_rida = [start]
        jelenlegi = start
        iranyok = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Fel, Le, Balra, Jobbra
        jelenlegi_irany = None

        # 2. Kezdeti irány meghatározása a 6-os pontból (merre van az első 0 vagy 5)
        for dr, dc in iranyok:
            nr, nc = start[0] + dr, start[1] + dc
            if 0 <= nr < self.sorok and 0 <= nc < self.oszlopok:
                if self.adatok[nr][nc] in [0, 5]:
                    jelenlegi_irany = (dr, dc)
                    break

        if not jelenlegi_irany:
            return []

        # 3. Végigmegyünk az úton a "mindig egyenesen, amíg lehet" szabállyal
        biztonsagi_fek = 0
        while jelenlegi != end and biztonsagi_fek < 1000:
            biztonsagi_fek += 1
            dr, dc = jelenlegi_irany
            elore_r, elore_c = jelenlegi[0] + dr, jelenlegi[1] + dc

            # Ha tudunk egyenesen menni (út vagy cél), akkor arra megyünk
            if (0 <= elore_r < self.sorok and 0 <= elore_c < self.oszlopok and 
                self.adatok[elore_r][elore_c] in [0, 5]):
                jelenlegi = (elore_r, elore_c)
                utvonal_rida.append(jelenlegi)
            else:
                # Kanyarodás: keressünk egy új irányt (kivéve amerre jöttünk)
                talalt = False
                for uj_dr, uj_dc in iranyok:
                    if uj_dr == -dr and uj_dc == -dc:  # Ne menjünk visszafelé
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
                    break # Zsákutca esetén megáll

        # 4. Rács koordináták konvertálása pixel koordinátákká (a cella közepe)
        pixel_utvonal = []
        for r, c in utvonal_rida:
            px = c * RACS_MERET + (RACS_MERET // 2)
            py = r * RACS_MERET + (RACS_MERET // 2)
            pixel_utvonal.append((px, py))

        return pixel_utvonal
