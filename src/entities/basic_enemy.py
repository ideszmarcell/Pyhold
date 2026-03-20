from src.entities.enemy import Enemy, PIROS

class BasicEnemy(Enemy):
    def __init__(self, path):
        # Sima ellenség: marad a piros kör (HP +15% nehézítéshez)
        super().__init__(path, speed=3, hp=28, radius=15, color=PIROS)
    
    def get_reward(self):
        """Alapellenség jutalma: HP // 2 + 2 = 14 pénz (kiegyenlítéshez)"""
        return self.max_hp // 2 + 2