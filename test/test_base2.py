from backend.services.ai.base2 import AIProvider

# Dummy implementation
class DummyProvider(AIProvider):
    def generate_meal_plan(self, goals, inventory):
        return {
            "meals": [
                {"name": "Test Meal", "calories": 500, "protein": 30}
            ],
            "goals": goals,
            "inventory_used": inventory
        }

if __name__ == "__main__":
    goals = {"calories": 2000, "protein": 100}
    inventory = [{"item": "chicken", "quantity": 2}]

    provider = DummyProvider()
    result = provider.generate_meal_plan(goals, inventory)

    print("Generated Meal Plan:")
    print(result)
