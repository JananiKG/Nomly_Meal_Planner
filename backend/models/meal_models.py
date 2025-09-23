from pydantic import BaseModel, Field, field_validator
from typing import List


class Ingredient(BaseModel):
    name: str
    quantity: str = Field(..., description="Quantity with units like '150g', '2 cups', '3 pieces'")


class Meal(BaseModel):
    name: str
    calories: str = Field(..., description="Calories with unit like '350 kcal'")
    protein: str = Field(..., description="Protein with unit like '30g'")
    ingredients_used: List[Ingredient]
    notes: List[str] = []


class MealPlan(BaseModel):
    goals: dict
    meals: List[Meal]
    notes: List[str]

    @field_validator("meals")
    def validate_meals(cls, meals):
        if not meals:
            raise ValueError("MealPlan must contain at least one meal")
        return meals
