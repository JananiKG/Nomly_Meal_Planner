# backend/services/meal_planner.py

from typing import List
from pydantic import BaseModel, Field, ValidationError, field_validator
import json


# ----------------------------
# Step 1: Define Ingredient model
# ----------------------------
class Ingredient(BaseModel):
    name: str
    quantity: float = Field(..., description="Quantity in cups/grams/etc.")


# ----------------------------
# Step 2: Define Meal model
# ----------------------------
class Meal(BaseModel):
    name: str
    calories: int
    protein: int
    ingredients_used: List[Ingredient]


# ----------------------------
# Step 3: Define MealPlan model
# ----------------------------
class MealPlan(BaseModel):
    goals: dict
    meals: List[Meal]
    notes: List[str]

    # ✅ Example of Pydantic v2 style validation
    @field_validator("meals")
    def validate_meals(cls, meals):
        if not meals:
            raise ValueError("MealPlan must contain at least one meal")
        return meals


# ----------------------------
# Step 4: MealPlanner service class
# ----------------------------
class MealPlanner:
    def build_prompt(self, goals: dict, inventory: List[str]) -> str:
        """
        Builds a natural language prompt to send to the AI model.
        """
        return (
            f"Generate a meal plan for goals {goals}. "
            f"Use only ingredients from this inventory: {', '.join(inventory)}. "
            f"Return output strictly as JSON with fields: goals, meals, notes."
        )

    def parse_response(self, response_text: str) -> MealPlan:
        """
        Parse AI JSON response into a structured MealPlan.
        """
        try:
            # Some AI providers wrap JSON in markdown ```json ... ```
            cleaned_text = response_text.strip("` \n")
            if cleaned_text.startswith("json"):
                cleaned_text = cleaned_text[4:]

            parsed = json.loads(cleaned_text)
            return MealPlan(**parsed)

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from AI: {e}")
        except ValidationError as e:
            raise ValueError(f"Response failed validation: {e}")
