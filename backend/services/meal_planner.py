# backend/services/meal_planner.py
from backend.services.ai.base import AIProvider
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ValidationError, field_validator
import json


# ----------------------------
# Step 1: Define Ingredient model
# ----------------------------
class Ingredient(BaseModel):
    name: str
    quantity: float | str = Field(..., description="Quantity in cups/grams/etc.")  # allow str or float


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
    def __init__(self, ai_client: AIProvider):
        self.ai_client = ai_client

    def build_prompt(self, goals: dict, inventory: List[str]) -> str:
        return (
            f"Generate a meal plan for goals {goals}. "
            f"Use only ingredients from this inventory: {', '.join(inventory)}. "
            f"Return output strictly as JSON with fields: goals, meals, notes."
        )

    def _normalize_ai_json(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Reshape AI output into strict MealPlan schema."""
        normalized_meals = []
        for m in raw.get("meals", []):
            # Handle alternate field names
            meal = {
                "name": m.get("name") or m.get("meal") or "Unknown Meal",
                "calories": m.get("calories") or m.get("cal", 0),
                "protein": m.get("protein", 0),
                "ingredients_used": []
            }

            # Handle ingredients: AI may return strings or dicts
            ingredients = m.get("ingredients_used") or m.get("items") or []
            normalized_ingredients = []
            for ing in ingredients:
                if isinstance(ing, str):
                    normalized_ingredients.append({"name": ing, "quantity": "1 unit"})
                elif isinstance(ing, dict):
                    normalized_ingredients.append({
                        "name": ing.get("name", "Unknown"),
                        "quantity": ing.get("quantity", "1 unit")
                    })
            meal["ingredients_used"] = normalized_ingredients

            normalized_meals.append(meal)

        # Ensure notes is always a list
        notes = raw.get("notes", [])
        if isinstance(notes, str):
            notes = [notes]

        return {
            "goals": raw.get("goals", {}),
            "meals": normalized_meals,
            "notes": notes
        }

    def parse_response(self, response_text: str) -> MealPlan:
        try:
            cleaned_text = response_text.strip("` \n")
            if cleaned_text.startswith("json"):
                cleaned_text = cleaned_text[4:]

            parsed_raw = json.loads(cleaned_text)
            normalized = self._normalize_ai_json(parsed_raw)
            return MealPlan(**normalized)

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from AI: {e}")
        except ValidationError as e:
            raise ValueError(f"Response failed validation: {e}")

    def generate_meal_plan(self, goals: dict, inventory: List[str]) -> MealPlan:
        prompt = self.build_prompt(goals, inventory)
        response_text = self.ai_client.generate(prompt)
        return self.parse_response(response_text)
