from fastapi import FastAPI
from backend.services.ai.gemini import GeminiProvider  # example
from backend.services.meal_planner import MealPlanner

app = FastAPI()

# Initialize AI provider (you’ll configure your API key etc. inside)
ai_client = GeminiProvider()

# Create MealPlanner with AI client
meal_planner = MealPlanner(ai_client)

@app.post("/generate-meal-plan")
def generate_meal_plan(goals: dict, inventory: list[str]):
    try:
        plan = meal_planner.generate_meal_plan(goals, inventory)
        return plan.model_dump()  # Pydantic v2 way
    except Exception as e:
        return {"detail": f"Meal generation failed: {e}"}
