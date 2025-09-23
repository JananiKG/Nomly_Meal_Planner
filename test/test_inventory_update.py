#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.quantity_parser import calculate_inventory_updates, parse_quantity, subtract_quantities

def test_quantity_parsing():
    print("=== Testing Quantity Parsing ===")
    
    test_cases = [
        "150g",
        "2 cups", 
        "3 pieces",
        "1/2 cup",
        "0.5 liters"
    ]
    
    for case in test_cases:
        amount, unit = parse_quantity(case)
        print(f"{case} -> {amount} {unit}")

def test_quantity_subtraction():
    print("\n=== Testing Quantity Subtraction ===")
    
    test_cases = [
        ("400g", "150g"),
        ("2 cups", "1.5 cups"),
        ("6 pieces", "3 pieces"),
        ("1 cup", "1/2 cup")
    ]
    
    for available, used in test_cases:
        remaining = subtract_quantities(available, used)
        print(f"{available} - {used} = {remaining}")

def test_inventory_updates():
    print("\n=== Testing Inventory Updates ===")
    
    # Mock data
    original_inventory = [
        "chicken: 400g",
        "rice: 2 cups", 
        "broccoli: 300g",
        "eggs: 6 pieces"
    ]
    
    used_ingredients = [
        {"name": "chicken", "quantity": "150g"},
        {"name": "rice", "quantity": "1 cup"},
        {"name": "broccoli", "quantity": "100g"},
        {"name": "eggs", "quantity": "2 pieces"}
    ]
    
    updates = calculate_inventory_updates(original_inventory, used_ingredients)
    
    print("Original Inventory:")
    for name, qty in updates["before"].items():
        print(f"  {name}: {qty}")
    
    print("\nUsed Ingredients:")
    for name, qty in updates["used"].items():
        print(f"  {name}: {qty}")
    
    print("\nRemaining Inventory:")
    for name, qty in updates["remaining"].items():
        print(f"  {name}: {qty}")

if __name__ == "__main__":
    test_quantity_parsing()
    test_quantity_subtraction()
    test_inventory_updates()
    print("\n✅ All tests completed!")
