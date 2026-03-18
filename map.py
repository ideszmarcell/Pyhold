import pygame
from settings import (
    KEK,
    RACS_MERET,
    FEKETE,
    SZURKE,
    ZOLD,
    FEHER,
    MAZE,
    SZELESSEG,
    MAGASSAG,
)
from src.entities.tower import Tower
from src.entities.arc_tower import ArcTower
from src.entities.shock_tower import ShockTower
from src.entities.slow_tower import SlowTower

# pylint: disable=no-member


class Palya:
    def __init__(self) -> None:
        self.oszlopok: int = len(MAZE[0])
        self.sorok: int = len(MAZE)
        self.adatok: list[list[int]] = [row[:] for row in MAZE]
        # Torny képválasztások tárolása: (r, c) -> image_type
        self.tower_images: dict[tuple[int, int], str] = {}
        # Torony objektumok tárolása
        self.tornyok: list[Tower] = []
        
        # Térkép mérete pixelben
        self.map_width = self.oszlopok * RACS_MERET
        self.map_height = self.sorok * RACS_MERET
        
        # Offset a térkép középre pozicionálásához
        self.offset_x = (SZELESSEG - self.map_width) // 2
        self.offset_y = (MAGASSAG - self.map_height) // 2

    def koordinata_szamitas(self, pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        # Adjustjuk az offset-et
        x -= self.offset_x
        y -= self.offset_y
        return x // RACS_MERET, y // RACS_MERET

    def _get_tower_block_top_left(self, r: int, c: int) -> tuple[int, int] | None:
        """
        Megtalálja a 2x2 torony blokk bal felső sarkát.
        Ha a cella torony (2), visszatér a blokk bal felső koordinátájával, egyébként None-t ad vissza.
        """
        if (
            not (0 <= r < self.sorok and 0 <= c < self.oszlopok)
            or self.adatok[r][c] != 2
        ):
            return None

        # Keress meg a 2x2 blokk bal felső sarkát
        top_r, top_c = r, c

        # Ellenőrizd, ha ez nem a bal felső sarok
        if r > 0 and c > 0 and self.adatok[r - 1][c - 1] == 2:
            top_r, top_c = r - 1, c - 1
        elif r > 0 and c + 1 < self.oszlopok and self.adatok[r - 1][c] == 2:
            top_r, top_c = r - 1, c
        elif c > 0 and r + 1 < self.sorok and self.adatok[r][c - 1] == 2:
            top_r, top_c = r, c - 1

        return (top_r, top_c)

    def get_tower_image(self, r: int, c: int) -> str | None:
        """Visszaadja a torony képét egy adott cellához. Ha nincs kiválasztva, None-t ad vissza."""
        tower_block = self._get_tower_block_top_left(r, c)
        if tower_block is None:
            return None
        return self.tower_images.get(tower_block, None)

    def set_tower_image(self, r: int, c: int, image_type: str) -> bool:
        """Beállítja a torony képét egy adott cellához és létrehozza az objektumot."""
        tower_block = self._get_tower_block_top_left(r, c)
        if tower_block is None:
            return False
        
        # Torony képének beállítása
        self.tower_images[tower_block] = image_type
        
        # Torony objektum keresése vagy létrehozása
        # A torony a bal felső sarknál helyezkedi el (tower_block)
        torony = None
        for t in self.tornyok:
            if t.gx == tower_block[1] and t.gy == tower_block[0]:
                torony = t
                break
        
        # Ha nem létezik, hozz létre a megfelelő típussal
        if torony is None:
            # Pilóta Tower Factory - megfelelő osztályt hoz létre
            if image_type == "arc":
                torony = ArcTower(tower_block[1], tower_block[0])
            elif image_type == "shock":
                torony = ShockTower(tower_block[1], tower_block[0])
            elif image_type == "slow":
                torony = SlowTower(tower_block[1], tower_block[0])
            else:
                torony = ArcTower(tower_block[1], tower_block[0])  # Alapértelmezett
            
            self.tornyok.append(torony)
        else:
            # Ha már létezik, cseréld le az új típusúra
            self.tornyok.remove(torony)
            if image_type == "arc":
                torony = ArcTower(tower_block[1], tower_block[0])
            elif image_type == "shock":
                torony = ShockTower(tower_block[1], tower_block[0])
            elif image_type == "slow":
                torony = SlowTower(tower_block[1], tower_block[0])
            else:
                torony = ArcTower(tower_block[1], tower_block[0])
            
            self.tornyok.append(torony)
        
        return True

    def remove_tower(self, tower: Tower) -> None:
        """Eltávolítja a tornyot a pályáról (map + torony lista + képállapot)."""
        # Töröljük a 2x2 torony blokkot a pályarácsból
        for dr in range(tower.size):
            for dc in range(tower.size):
                r = tower.gy + dr
                c = tower.gx + dc
                if 0 <= r < self.sorok and 0 <= c < self.oszlopok and self.adatok[r][c] == 2:
                    self.adatok[r][c] = 0

        # Távolítsuk el a torony objektumot
        if tower in self.tornyok:
            self.tornyok.remove(tower)

        # Töröljük a torony kép hozzárendelést is
        self.tower_images.pop((tower.gy, tower.gx), None)

    def cella_modositas(self, pos: tuple[int, int]) -> None:
        gx, gy = self.koordinata_szamitas(pos)
        if 0 <= gy < self.sorok and 0 <= gx < self.oszlopok:
            self.adatok[gy][gx] = 1 if self.adatok[gy][gx] == 0 else 0

    def afectar_tornya_blokk(self, pos: tuple[int, int]) -> bool:
        """Hatást gyakorol az összekapcsolt toronyblokkra.

        Ha van olyan torony objektum a listában, amelynek bal felső koordinátája
egyezik a blokkéval, azt is eltávolítjuk.
        """
        gx, gy = self.koordinata_szamitas(pos)

        # Ellenőrizd, hogy ez a cella torony-e
        if (
            not (0 <= gy < self.sorok and 0 <= gx < self.oszlopok)
            or self.adatok[gy][gx] != 2
        ):
            return False

        # Keresd meg a 2x2 blokk bal felső sarkát
        top_r, top_c = gy, gx
        if gy > 0 and gx > 0 and self.adatok[gy - 1][gx - 1] == 2:
            top_r, top_c = gy - 1, gx - 1
        elif gy > 0 and gx + 1 < self.oszlopok and self.adatok[gy - 1][gx] == 2:
            top_r, top_c = gy - 1, gx
        elif gx > 0 and gy + 1 < self.sorok and self.adatok[gy][gx - 1] == 2:
            top_r, top_c = gy, gx - 1

        # Próbáljuk meg eltávolítani a megfelelő torony objektumot
        for torony in list(self.tornyok):
            if torony.gx == top_c and torony.gy == top_r:
                self.remove_tower(torony)
                return True

        # Ha nincs torony objektum, akkor legalább a pályarácsból távolítsuk el
        for dr in range(2):
            for dc in range(2):
                nr, nc = top_r + dr, top_c + dc
                if (
                    0 <= nr < self.sorok
                    and 0 <= nc < self.oszlopok
                    and self.adatok[nr][nc] == 2
                ):
                    self.adatok[nr][nc] = 0  # Torony eltávolítása

        return True

    def _rajzol_vonalak(self, felulet: pygame.Surface) -> None:
        for x in range(0, self.oszlopok * RACS_MERET + 1, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (x + self.offset_x, self.offset_y), (x + self.offset_x, self.sorok * RACS_MERET + self.offset_y))
        for y in range(0, self.sorok * RACS_MERET + 1, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (self.offset_x, y + self.offset_y), (self.oszlopok * RACS_MERET + self.offset_x, y + self.offset_y))

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

                        # Torony rajzolása képpel
                        self._rajzol_torony_keppel(felulet, c, r, szelesseg, magassag)
                        continue
                elif self.adatok[r][c] == 3:  # Speciális épület
                    szin = KEK
                elif self.adatok[r][c] == 6:  # Kezdőpont
                    szin = FEHER
                elif self.adatok[r][c] == 5:  # Végpont (Bázis)
                    szin = (255, 50, 50)
                else:
                    # BIZTONSÁGI HÁLÓ: Ha ismeretlen szám van a pályán, legyen rikító lila!
                    szin = (255, 0, 255)

                if szin:
                    # Rajzolás
                    rect = pygame.Rect(
                        c * RACS_MERET + self.offset_x, r * RACS_MERET + self.offset_y, szelesseg, magassag
                    )
                    pygame.draw.rect(felulet, szin, rect)

                    rect = (
                        c * RACS_MERET + 1 + self.offset_x,
                        r * RACS_MERET + 1 + self.offset_y,
                        szelesseg - 2,
                        magassag - 2,
                    )
                    pygame.draw.rect(felulet, szin, rect)

    def _rajzol_torony_keppel(
        self, felulet: pygame.Surface, c: int, r: int, szelesseg: int, magassag: int
    ) -> None:
        """Kirajzolja a tornyot képpel vagy fallback-kel."""
        # Kérj az kiválasztott kép típusát
        image_type = self.get_tower_image(r, c)

        # Ha van kiválasztott kép, rajzold meg
        if image_type is not None and image_type in Tower._images_cache:
            try:
                # Méretezd a képet, hogy foglalkozzon a 2x2 mérettel
                img = Tower._images_cache[image_type]
                scaled_img = pygame.transform.scale(img, (szelesseg - 8, magassag - 8))
                felulet.blit(scaled_img, (c * RACS_MERET + 4 + self.offset_x, r * RACS_MERET + 4 + self.offset_y))
            except Exception as e:
                print(f"Hiba a torony képének rajzolásánál: {e}")
                self._rajzol_torony_alapertelmezett(felulet, c, r, szelesseg, magassag)
        else:
            # Ha nincs kiválasztott kép, vagy a kép nincs az cache-ben, rajzolj alapértelmezést
            self._rajzol_torony_alapertelmezett(felulet, c, r, szelesseg, magassag)

    def _rajzol_torony_alapertelmezett(
        self, felulet: pygame.Surface, c: int, r: int, szelesseg: int, magassag: int
    ) -> None:
        """Az alapértelmezett torony ábra (zöld négyzet)."""
        rect = pygame.Rect(c * RACS_MERET + self.offset_x, r * RACS_MERET + self.offset_y, szelesseg, magassag)
        pygame.draw.rect(felulet, ZOLD, rect)

        rect_inner = (
            c * RACS_MERET + 1 + self.offset_x,
            r * RACS_MERET + 1 + self.offset_y,
            szelesseg - 2,
            magassag - 2,
        )
        pygame.draw.rect(felulet, ZOLD, rect_inner)

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
