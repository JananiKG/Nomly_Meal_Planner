#!/usr/bin/env python3

import sys
import os
sys.path.append('/root/Nomly_Meal_Planner')

from backend.utils.quantity_parser import calculate_inventory_updates

def test_overconsumption():
    print("=== TESTING OVER-CONSUMPTION SCENARIOS ===")
    
    # Scenario 1: Clear over-consumption
    inventory = ["chicken: 100g", "rice: 1 cup"]
    used = [
        {"name": "chicken", "quantity": "200g"},  # Need 200g, have 100g
        {"name": "rice", "quantity": "2 cups"}   # Need 2 cups, have 1 cup
    ]
    
    updates = calculate_inventory_updates(inventory, used)
    
    print("Inventory:", inventory)
    print("Used:", used)
    print("Remaining:", updates["remaining"])
    print("Warnings:", updates.get("warnings", []))
    
    # Scenario 2: Mixed valid and invalid
    print("\n=== MIXED SCENARIO ===")
    inventory2 = ["chicken: 300g", "rice: invalid", "eggs: 2 pieces"]
    used2 = [
        {"name": "chicken", "quantity": "150g"},  # Valid
        {"name": "rice", "quantity": "1 cup"},    # Invalid original
        {"name": "eggs", "quantity": "5 pieces"}, # Over-consumption
        {"name": "beef", "quantity": "100g"}      # Not in inventory
    ]
    
    updates2 = calculate_inventory_updates(inventory2, used2)
    print("Remaining:", updates2["remaining"])
    print("Warnings:", updates2.get("warnings", []))

if __name__ == "__main__":
    test_overconsumption()
