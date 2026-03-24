"""Factory for creating towers."""
from entities.arc_tower import ArcTower
from entities.shock_tower import ShockTower
from entities.slow_tower import SlowTower


class TowerFactory:
    """Factory for creating tower instances."""
    
    TOWER_TYPES = {
        'arc': ArcTower,
        'shock': ShockTower,
        'slow': SlowTower,
    }
    
    @staticmethod
    def create(tower_type: str, gx: int, gy: int):
        """Create a tower of the specified type at given coordinates."""
        if tower_type not in TowerFactory.TOWER_TYPES:
            raise ValueError(f"Unknown tower type: {tower_type}")
        
        tower_class = TowerFactory.TOWER_TYPES[tower_type]
        return tower_class(gx, gy)
    
    @staticmethod
    def get_tower_types() -> list[str]:
        """Get list of available tower types."""
        return list(TowerFactory.TOWER_TYPES.keys())
    
    @staticmethod
    def get_tower_cost(tower_type: str) -> int:
        """Get cost for a tower type."""
        from core.settings import TOWER_COST
        return TOWER_COST  # All towers have same cost
