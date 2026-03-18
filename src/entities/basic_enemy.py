from src.entities.enemy import Enemy, PIROS

class BasicEnemy(Enemy):
    def __init__(self, path):
        # Sima ellenség: marad a piros kör
        super().__init__(path, speed=3, hp=24, radius=15, color=PIROS)