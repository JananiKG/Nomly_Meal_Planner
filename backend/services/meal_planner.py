from backend.models.meal_models import MealPlan
from backend.services.ai.base import AIProvider
from backend.utils.quantity_parser import calculate_inventory_updates
from typing import List, Dict, Any
from pydantic import ValidationError


class MealPlanner:
    def __init__(self, ai_client: AIProvider, safe_mode: bool = False):
        """
        :param ai_client: AI provider client
        :param safe_mode: if True → skip invalid meals instead of failing
        """
        self.ai_client = ai_client
        self.safe_mode = safe_mode

    def generate_meal_plan(self, goals: dict, inventory: List[str]) -> Dict[str, Any]:
        """Generate meal plan using AI provider and calculate inventory updates"""
        try:
            # AI provider handles all prompt building and parsing
            plan_dict = self.ai_client.generate_meal_plan(goals, inventory)
            
            # Validate and create structured meal plan
            meal_plan = MealPlan(**plan_dict)
            
            # Calculate inventory updates
            all_used_ingredients = []
            for meal in meal_plan.meals:
                all_used_ingredients.extend([
                    {"name": ing.name, "quantity": ing.quantity} 
                    for ing in meal.ingredients_used
                ])
            
            inventory_updates = calculate_inventory_updates(inventory, all_used_ingredients)
            
            # Return enhanced response with inventory updates
            return {
                "meal_plan": meal_plan.model_dump(),
                "inventory_updates": inventory_updates
            }
            
        except ValidationError as ve:
            # Let FastAPI handle the JSON serialization
            raise ve
        except Exception as e:
            raise ValueError(f"Meal generation failed: {e}")
