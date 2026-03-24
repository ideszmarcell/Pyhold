"""Factory for creating enemies."""
from entities.basic_enemy import BasicEnemy
from entities.fast_enemy import FastEnemy
from entities.tank_enemy import TankEnemy
from entities.armored_enemy import ArmoredEnemy
from entities.boss_enemy import BossEnemy


class EnemyFactory:
    """Factory for creating enemy instances."""
    
    ENEMY_TYPES = {
        'basic': BasicEnemy,
        'fast': FastEnemy,
        'tank': TankEnemy,
        'armored': ArmoredEnemy,
    }
    
    @staticmethod
    def create(enemy_type: str, path: list[tuple[int, int]]):
        """Create an enemy of the specified type."""
        if enemy_type not in EnemyFactory.ENEMY_TYPES:
            raise ValueError(f"Unknown enemy type: {enemy_type}")
        
        enemy_class = EnemyFactory.ENEMY_TYPES[enemy_type]
        return enemy_class(path)
    
    @staticmethod
    def create_boss(path: list[tuple[int, int]], wave: int):
        """Create a boss enemy."""
        return BossEnemy(path, wave=wave)
    
    @staticmethod
    def get_enemy_types() -> list[str]:
        """Get list of available enemy types."""
        return list(EnemyFactory.ENEMY_TYPES.keys())
