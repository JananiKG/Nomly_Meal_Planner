import os
import json
import google.generativeai as genai
from typing import Dict, List, Any
from .base import AIProvider


class GeminiProvider(AIProvider):
    """
    Gemini implementation of AIProvider interface.
    """

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def _build_prompt(self, goals: dict, inventory: List[str]) -> str:
        """Build Gemini-optimized prompt"""
        return (
            "You are a nutrition assistant.\n"
            f"Generate a DAILY meal plan for these goals: {goals}.\n"
            f"Use only ingredients from this inventory: {', '.join(inventory)}.\n\n"
            "Strictly follow this JSON schema:\n"
            "{\n"
            "  'goals': { 'calories': int, 'protein': int },\n"
            "  'meals': [\n"
            "    {\n"
            "      'name': string,\n"
            "      'calories': string,\n"
            "      'protein': string,\n"
            "      'items': [\n"
            "        { 'food': string, 'quantity': string }\n"
            "      ],\n"
            "      'notes': [string]\n"
            "    }\n"
            "  ],\n"
            "  'notes': [string]\n"
            "}\n\n"
            "Important rules:\n"
            "1. Every meal MUST include ingredients from inventory in 'items' field.\n"
            "2. Use 'food' for ingredient name, 'quantity' MUST include units like '150g', '2 cups', '250ml', '3 pieces'.\n"
            "3. Calculate calories and protein with units like '350 kcal', '30g protein'.\n"
            "4. In 'notes' field for each meal, provide detailed recipe with title and step-by-step instructions.\n"
            "5. Return only valid JSON, no explanations.\n\n"
            "Example detailed recipe format:\n"
            "\"notes\": [\"Chicken Teriyaki Bowl\", \"1. Season 200g chicken with salt and pepper\", \"2. Heat oil in pan over medium-high heat\", \"3. Cook chicken 6-7 minutes per side until golden\", \"4. Meanwhile, cook 1 cup rice according to package directions\", \"5. Steam 100g broccoli for 4-5 minutes until tender-crisp\", \"6. Slice chicken and serve over rice with broccoli\"]\n"
        )

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response and normalize to expected format"""
        cleaned_text = response_text.strip("` \n")
        if cleaned_text.startswith("json"):
            cleaned_text = cleaned_text[4:]

        parsed = json.loads(cleaned_text)

        # Normalize plan-level notes
        if "notes" in parsed and isinstance(parsed["notes"], str):
            parsed["notes"] = [parsed["notes"]]
        elif "notes" not in parsed:
            parsed["notes"] = []

        # Normalize meals
        meals = parsed.get("meals", [])
        normalized_meals = []

        for meal in meals:
            # Map 'items' -> 'ingredients_used'
            items = meal.pop("items", [])
            ingredients_used = []
            for item in items:
                ingredients_used.append({
                    "name": item.get("food", "Unknown"),
                    "quantity": item.get("quantity", "0")
                })

            # Ensure meal-level notes exists and is a list
            meal_notes = meal.get("notes", [])
            if isinstance(meal_notes, str):
                meal_notes = [meal_notes]
            elif meal_notes is None:
                meal_notes = []

            normalized_meals.append({
                "name": meal.get("name", "Unnamed Meal"),
                "calories": meal.get("calories", "0 kcal"),
                "protein": meal.get("protein", "0g"),
                "ingredients_used": ingredients_used,
                "notes": meal_notes
            })

        parsed["meals"] = normalized_meals
        return parsed

    def generate_meal_plan(self, goals: Dict[str, Any], inventory: List[str]) -> Dict[str, Any]:
        """Generate meal plan using Gemini with provider-specific logic"""
        prompt = self._build_prompt(goals, inventory)
        response = self.model.generate_content(prompt)
        return self._parse_response(response.text)
