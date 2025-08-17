# test/test_meal_planner.py

from backend.services.meal_planner import MealPlanner

# Simulated AI Response (like Gemini would return)
fake_ai_response = """
{
  "goals": {"calories": 2000, "protein": 100},
  "meals": [
    {
      "name": "Chicken and Broccoli Stir-fry with Rice",
      "calories": 750,
      "protein": 60,
      "ingredients_used": [
        {"name": "chicken breast", "quantity": 1},
        {"name": "rice", "quantity": 0.5},
        {"name": "broccoli", "quantity": 2}
      ]
    },
    {
      "name": "Chicken Breast Salad",
      "calories": 600,
      "protein": 30,
      "ingredients_used": [
        {"name": "chicken breast", "quantity": 1},
        {"name": "broccoli", "quantity": 1}
      ]
    },
    {
      "name": "Leftover Chicken and Rice",
      "calories": 650,
      "protein": 10,
      "ingredients_used": [
        {"name": "rice", "quantity": 0.5},
        {"name": "chicken breast", "quantity": 0}
      ]
    }
  ],
  "notes": [
    "This meal plan provides ~2000 calories and 100g of protein.",
    "Consider adding other vegetables or healthy fats."
  ]
}
"""

def manual_test_meal_planner():
    planner = MealPlanner()

    # Step 1: Build a prompt
    prompt = planner.build_prompt(
        goals={"calories": 2000, "protein": 100},
        inventory=["chicken breast", "rice", "broccoli"]
    )
    print("Prompt Sent to AI:")
    print(prompt)

    # Step 2: Parse AI response
    try:
        meal_plan = planner.parse_response(fake_ai_response)
        print("\n✅ Parsed Meal Plan:")
        print(meal_plan.model_dump_json(indent=2))  # Pydantic v2 uses model_dump_json
    except Exception as e:
        print("\n❌ Error while parsing:", e)


if __name__ == "__main__":
    manual_test_meal_planner()
