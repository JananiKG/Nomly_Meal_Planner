# backend/services/meal_planner.py
from backend.services.ai.base import AIProvider
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

    @field_validator("meals")
    def validate_meals(cls, meals):
        if not meals:
            raise ValueError("MealPlan must contain at least one meal")
        return meals


# ----------------------------
# Step 4: MealPlanner service class
# ----------------------------
class MealPlanner:
    def __init__(self, ai_client: AIProvider, safe_mode: bool = False):
        """
        :param ai_client: AI provider client
        :param safe_mode: if True → skip invalid meals instead of failing
        """
        self.ai_client = ai_client
        self.safe_mode = safe_mode

    def build_prompt(self, goals: dict, inventory: List[str]) -> str:
        return (
            f"Generate a meal plan for goals {goals}. "
            f"Use only ingredients from this inventory: {', '.join(inventory)}. "
            f"Return output strictly as JSON with fields: goals, meals, notes."
        )

    def parse_response(self, response_text: str) -> MealPlan:
        cleaned_text = response_text.strip("` \n")
        if cleaned_text.startswith("json"):
            cleaned_text = cleaned_text[4:]

        try:
            parsed = json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from AI: {e}")

        if not self.safe_mode:
            # Strict validation (fail fast)
            try:
                return MealPlan(**parsed)
            except ValidationError as e:
                raise ValueError(f"Response failed validation: {e}")
        else:
            # Safe mode: try to salvage valid meals
            valid_meals = []
            for meal in parsed.get("meals", []):
                try:
                    valid_meals.append(Meal(**meal))
                except ValidationError:
                    continue  # skip invalid meal

            return MealPlan(
                goals=parsed.get("goals", {}),
                meals=valid_meals,
                notes=parsed.get("notes", []),
            )

    def generate_meal_plan(self, goals: dict, inventory: List[str]) -> MealPlan:
        prompt = self.build_prompt(goals, inventory)
        response_text = self.ai_client.generate(prompt)
        return self.parse_response(response_text)
