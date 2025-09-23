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
    notes: list[str] = [] 


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

    #def parse_response(self, response_text: str) -> MealPlan:
        try:
            cleaned_text = response_text.strip("` \n")
            if cleaned_text.startswith("json"):
                cleaned_text = cleaned_text[4:]

            parsed = json.loads(cleaned_text)
            return MealPlan(**parsed)

        except json.JSONDecodeError as e:
            # return as structured list
            raise ValidationError([{
                "loc": ("response_text",),
                "msg": f"Invalid JSON from AI: {e}",
                "type": "json_error"
            }], model=MealPlan)

        except ValidationError as e:
            # propagate as is (FastAPI will serialize nicely)
            raise e

    #def parse_response(self, response_text: str) -> MealPlan:
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

    #def parse_response(self, response_text: str) -> MealPlan:
        """
        Parse AI JSON response into a structured MealPlan and normalize it
        so it matches our Pydantic models.
        """
        try:
            import json
            cleaned_text = response_text.strip("` \n")
            if cleaned_text.startswith("json"):
                cleaned_text = cleaned_text[4:]

            parsed = json.loads(cleaned_text)

            # --------------------------
            # Normalization starts here
            # --------------------------
            # Ensure notes is a list
            if "notes" in parsed and isinstance(parsed["notes"], str):
                parsed["notes"] = [parsed["notes"]]

            # Ensure meals is a list
            meals = parsed.get("meals", [])
            normalized_meals = []

            for meal in meals:
                # Map 'items' -> 'ingredients_used'
                items = meal.pop("items", [])
                ingredients_used = []
                for item in items:
                    ingredients_used.append({
                        "name": item.get("food", "Unknown"),
                        "quantity": self._parse_quantity(item.get("quantity", 0))
                    })

                # Provide defaults for calories and protein
                calories = meal.get("calories", 0)
                protein = meal.get("protein", 0)

                normalized_meals.append({
                    "name": meal.get("name", "Unnamed Meal"),
                    "calories": calories,
                    "protein": protein,
                    "ingredients_used": ingredients_used
                })

            parsed["meals"] = normalized_meals

            return MealPlan(**parsed)

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from AI: {e}")
        except ValidationError as e:
            raise ValueError(f"Response failed validation: {e}")

    # Helper method to convert quantity string to float
    #def _parse_quantity(self, qty_str: str) -> float:
        """
        Extract a numeric value from a string like "3 whole eggs" -> 3
        """
        import re
        match = re.search(r"[\d\.]+", str(qty_str))
        return float(match.group()) if match else 0

    def parse_response(self, response_text: str) -> MealPlan:
        """
        Parse AI JSON response into a structured MealPlan and normalize it
        so it matches our Pydantic models.
        """
        try:
            import json
            cleaned_text = response_text.strip("` \n")
            if cleaned_text.startswith("json"):
                cleaned_text = cleaned_text[4:]
    
            parsed = json.loads(cleaned_text)
    
            # --------------------------
            # Normalize plan-level notes
            # --------------------------
            if "notes" in parsed and isinstance(parsed["notes"], str):
                parsed["notes"] = [parsed["notes"]]
            elif "notes" not in parsed:
                parsed["notes"] = []
    
            # --------------------------
            # Normalize meals
            # --------------------------
            meals = parsed.get("meals", [])
            normalized_meals = []
    
            for meal in meals:
                # Map 'items' -> 'ingredients_used'
                items = meal.pop("items", [])
                ingredients_used = []
                for item in items:
                    ingredients_used.append({
                        "name": item.get("food", "Unknown"),
                        "quantity": self._parse_quantity(item.get("quantity", 0))
                    })
    
                # Provide defaults for calories and protein
                calories = meal.get("calories", 0)
                protein = meal.get("protein", 0)
    
                # Ensure meal-level notes exists and is a list
                meal_notes = meal.get("notes", [])
                if isinstance(meal_notes, str):
                    meal_notes = [meal_notes]
                elif meal_notes is None:
                    meal_notes = []
    
                normalized_meals.append({
                    "name": meal.get("name", "Unnamed Meal"),
                    "calories": calories,
                    "protein": protein,
                    "ingredients_used": ingredients_used,
                    "notes": meal_notes  # <-- added meal-level notes
                })
    
            parsed["meals"] = normalized_meals
    
            return MealPlan(**parsed)
    
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON from AI: {e}")
        except ValidationError as e:
            raise ValueError(f"Response failed validation: {e}")
    
    # Helper method to convert quantity string to float
    def _parse_quantity(self, qty_str: str) -> float:
        """
        Extract a numeric value from a string like "3 whole eggs" -> 3
        """
        import re
        match = re.search(r"[\d\.]+", str(qty_str))
        return float(match.group()) if match else 0
    


    def generate_meal_plan(self, goals: dict, inventory: List[str]) -> MealPlan:
        prompt = self.build_prompt(goals, inventory)
        response_text = self.ai_client.generate(prompt)
        #return self.parse_response(response_text)
        try:
            return self.parse_response(response_text)
        except ValidationError as ve:
            # Let FastAPI handle the JSON serialization
            raise ve  # Do NOT wrap in ValueError
