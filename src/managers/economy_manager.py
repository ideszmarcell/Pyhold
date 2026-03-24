"""Economy management for the game"""


class EconomyManager:
    """Manages game currency and finances."""
    
    def __init__(self, starting_money: int = 200):
        self.money = starting_money
        self.transaction_history = []
    
    def can_afford(self, cost: int) -> bool:
        """Check if player can afford something."""
        return self.money >= cost
    
    def spend(self, cost: int, description: str = "") -> bool:
        """Spend money if affordable."""
        if self.can_afford(cost):
            self.money -= cost
            self.transaction_history.append((-cost, description))
            return True
        return False
    
    def earn(self, amount: int, description: str = "") -> None:
        """Earn money."""
        self.money += amount
        self.transaction_history.append((amount, description))
    
    def get_balance(self) -> int:
        """Get current balance."""
        return self.money
    
    def reset(self) -> None:
        """Reset economy for new game."""
        self.money = 200
        self.transaction_history = []
