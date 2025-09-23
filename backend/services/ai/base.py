from abc import ABC, abstractmethod
from typing import Dict, List, Any

class AIProvider(ABC):
    """
    Base interface for all AI providers (e.g., Gemini, OpenAI).
    """

    @abstractmethod
    def generate_meal_plan(self, goals: Dict[str, Any], inventory: List[str]) -> Dict[str, Any]:
        """
        Generate a meal plan based on user goals and current inventory.
        :param goals: Dict with user goals (calories, protein, etc.)
        :param inventory: List of inventory items with quantities
        :return: Structured meal plan as a dictionary
        """
        pass
