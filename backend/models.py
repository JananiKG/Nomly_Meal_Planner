# Create models.py with Pydantic schemas for InventoryItem, InventoryList

from pydantic import BaseModel, Field
from typing import List, Optional

class InventoryItem(BaseModel):
    name: str = Field(..., description="Name of the ingredient or product")
    quantity: float = Field(..., ge=0, description="Available quantity in units (e.g., grams, pieces)")
    unit: str = Field(..., description="Unit of measurement (e.g., grams, pieces, ml)")
    calories: Optional[float] = Field(None, ge=0, description="Calories per unit or portion")
    protein: Optional[float] = Field(None, ge=0, description="Protein content per unit or portion")

class InventoryList(BaseModel):
    items: List[InventoryItem] = Field(..., description="List of all inventory items")
