import os
import google.generativeai as genai
from typing import Dict, List, Any
from .base2 import AIProvider


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

    def generate_meal_plan(self, goals: Dict[str, Any], inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a meal plan using Gemini.
        """
        prompt = f"""
        You are a meal planning assistant.
        User goals: {goals}
        Inventory: {inventory}

        Generate a structured meal plan in JSON format with fields:
        - goals
        - meals (list of meals with name, calories, protein, ingredients used)
        - notes
        """
        
        response = self.model.generate_content(prompt)

        # Gemini might return text → we try parsing JSON safely
        try:
            import json
            return json.loads(response.text)
        except Exception:
            return {"error": "Failed to parse response", "raw": response.text}
