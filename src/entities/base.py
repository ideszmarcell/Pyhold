"""Abstract entity base classes."""
from abc import ABC, abstractmethod
import pygame


class Drawable(ABC):
    """Interface for drawable objects."""
    
    @abstractmethod
    def draw(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0) -> None:
        """Draw the entity on the surface."""
        pass


class Updatable(ABC):
    """Interface for objects that update."""
    
    @abstractmethod
    def update(self) -> None:
        """Update entity state."""
        pass


class Damageable(ABC):
    """Interface for objects that can take damage."""
    
    @abstractmethod
    def take_damage(self, damage: int) -> bool:
        """Take damage. Returns True if dead."""
        pass
