from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

# Reuse your validated response model & service
from backend.services.meal_planner import MealPlanner, MealPlan
# Use your existing provider implementation from Task 2
from backend.services.ai.gemini import GeminiProvider  # adjust import if needed


router = APIRouter()


# ---------- Request Schemas (Pydantic v2) ----------

class InventoryItem(BaseModel):
    name: str = Field(..., min_length=1)
    qty: float = Field(..., ge=0)
    unit: Optional[str] = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        nv = v.strip()
        if not nv:
            raise ValueError("name cannot be empty")
        return nv


class GenerateMealRequest(BaseModel):
    # We mirror your Task 3 shapes: `goals` can include calories/protein/etc.
    goals: Dict[str, float]
    inventory: List[InventoryItem]
    date: Optional[str] = None  # optional override of plan date (YYYY-MM-DD)


# ---------- Endpoint ----------

@router.post("/generate", response_model=MealPlan, summary="Generate a 1-day meal plan")
async def generate_meal_plan(request: GenerateMealRequest):
    """
    Calls the AI provider via MealPlanner to generate a structured, validated meal plan.
    """
    try:
        provider = GeminiProvider()             # your Task 2 provider
        planner = MealPlanner(provider=provider)

        # Convert InventoryItem models to plain dicts for your planner
        inventory_payload = [item.model_dump() for item in request.inventory]

        # Call your Task 3 planner
        plan_dict = planner.generate_meal_plan(
            goals=request.goals,
            inventory=inventory_payload,
            plan_date=request.date
        )

        # FastAPI will coerce this dict into the MealPlan response_model
        return plan_dict

    except Exception as e:
        # Bubble a readable error to the client
        raise HTTPException(status_code=500, detail=f"Meal generation failed: {e}")
