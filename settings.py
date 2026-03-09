import pygame

# --- KONSTANSOK ---
SZELESSEG, MAGASSAG = 800, 600
RACS_MERET = 40
FEKETE = (20, 20, 25)
SZURKE = (40, 40, 50)
ZOLD = (34, 139, 34)
VILAGOS_SZURKE = (60, 60, 70)

class Palya:
    def __init__(self):
        self.oszlopok = SZELESSEG // RACS_MERET
        self.sorok = MAGASSAG // RACS_MERET
        # 2D lista létrehozása: 0 = üres, 1 = épület
        self.adatok = [[0 for _ in range(self.oszlopok)] for _ in range(self.sorok)]

    # Clean Code: Pixelt vált át rács-indexre
    def koordinata_szamitas(self, pos):
        x, y = pos
        return x // RACS_MERET, y // RACS_MERET

    # Clean Code: Egy cella állapotának megváltoztatása
    def cella_modositas(self, pos):
        gx, gy = self.koordinata_szamitas(pos)
        if 0 <= gy < self.sorok and 0 <= gx < self.oszlopok:
            # Ha üres volt, legyen épület (1), ha épület volt, legyen üres (0)
            self.adatok[gy][gx] = 1 if self.adatok[gy][gx] == 0 else 0

    # Clean Code: Csak a rácsvonalakat rajzolja
    def _rajzol_vonalak(self, felulet):
        for x in range(0, SZELESSEG, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (x, 0), (x, MAGASSAG))
        for y in range(0, MAGASSAG, RACS_MERET):
            pygame.draw.line(felulet, SZURKE, (0, y), (SZELESSEG, y))

    # Clean Code: Csak a beépített cellákat rajzolja
    def _rajzol_epuletek(self, felulet):
        for r in range(self.sorok):
            for c in range(self.oszlopok):
                if self.adatok[r][c] == 1:
                    rect = (c * RACS_MERET + 2, r * RACS_MERET + 2, RACS_MERET - 4, RACS_MERET - 4)
                    pygame.draw.rect(felulet, ZOLD, rect)

    def rajzol(self, felulet):
        felulet.fill(FEKETE)
        self._rajzol_epuletek(felulet)
        self._rajzol_vonalak(felulet)

class Jatek:
    def __init__(self):
        pygame.init()
        self.ablak = pygame.display.set_mode((SZELESSEG, MAGASSAG))
        pygame.display.set_caption("Outhold Pálya Rendszer")
        self.palya = Palya()
        self.futo = True

    def esemenyek(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.futo = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.palya.cella_modositas(event.pos)

    def futtat(self):
        while self.futo:
            self.esemenyek()
            self.palya.rajzol(self.ablak)
            pygame.display.update()
        pygame.quit()

# --- INDÍTÁS ---
if __name__ == "__main__":
    app = Jatek()
    app.futtat()