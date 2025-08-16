from abc import ABC, abstractmethod
from typing import Any

class AIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> Any:
        """Generate a meal plan from the given prompt."""
        pass