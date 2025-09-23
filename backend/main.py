from fastapi import FastAPI
from backend.services.ai.gemini import GeminiProvider
from backend.services.meal_planner import MealPlanner
from pydantic import ValidationError

app = FastAPI()

# Initialize AI provider
ai_client = GeminiProvider()

# Create MealPlanner with AI client
meal_planner = MealPlanner(ai_client, safe_mode=False)

@app.post("/generate-meal-plan")
def generate_meal_plan(goals: dict, inventory: list[str]):
    try:
        # Returns dict with meal_plan and inventory_updates
        result = meal_planner.generate_meal_plan(goals, inventory)
        return result
    except ValidationError as ve:
        # Properly structured JSON for errors
        return {"detail": ve.errors()}
    except Exception as e:
        return {"detail": str(e)}
