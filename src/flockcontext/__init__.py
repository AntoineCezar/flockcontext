import importlib.metadata

from .flock import Flock
from .flock_open import FlockOpen

__version__ = importlib.metadata.version("flockcontext")

__all__ = [
    "Flock",
    "FlockOpen",
]
