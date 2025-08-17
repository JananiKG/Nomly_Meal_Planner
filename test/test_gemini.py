import os
import json
import re
from backend.services.ai.gemini import GeminiProvider

def main():
    provider = GeminiProvider()

    goals = {"calories": 2000, "protein": 100}
    inventory = [
        {"name": "chicken breast", "quantity": 2},
        {"name": "rice", "quantity": 1},
        {"name": "broccoli", "quantity": 3},
    ]

    print("🔹 Sending request to Gemini...")
    result = provider.generate_meal_plan(goals, inventory)

    raw_output = result.get("raw", result)

    # If raw_output contains markdown ```json fences → remove them
    if isinstance(raw_output, str):
        cleaned = re.sub(r"^```json|```$", "", raw_output, flags=re.MULTILINE).strip()
        try:
            parsed = json.loads(cleaned)
            print("\n✅ Gemini Response (Parsed JSON):")
            print(json.dumps(parsed, indent=4))
        except Exception:
            print("\n⚠️ Could not parse JSON. Showing cleaned text:")
            print(cleaned)
    else:
        print("\n✅ Gemini Response (Already JSON):")
        print(json.dumps(raw_output, indent=4))


if __name__ == "__main__":
    main()
