from backend.models.meal_models import MealPlan
from backend.services.ai.base import AIProvider
from typing import List
from pydantic import ValidationError


class MealPlanner:
    def __init__(self, ai_client: AIProvider, safe_mode: bool = False):
        """
        :param ai_client: AI provider client
        :param safe_mode: if True → skip invalid meals instead of failing
        """
        self.ai_client = ai_client
        self.safe_mode = safe_mode

    def generate_meal_plan(self, goals: dict, inventory: List[str]) -> MealPlan:
        """Generate meal plan using AI provider and validate with Pydantic"""
        try:
            # AI provider handles all prompt building and parsing
            plan_dict = self.ai_client.generate_meal_plan(goals, inventory)
            
            # Validate and return structured meal plan
            return MealPlan(**plan_dict)
            
        except ValidationError as ve:
            # Let FastAPI handle the JSON serialization
            raise ve
        except Exception as e:
            raise ValueError(f"Meal generation failed: {e}")
