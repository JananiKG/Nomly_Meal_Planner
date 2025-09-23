#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.quantity_parser import calculate_inventory_updates, parse_quantity, subtract_quantities

def test_edge_cases():
    print("=== TESTING EDGE CASES ===")
    
    # Edge Case 1: Using more than available
    print("\n1. Using more than available:")
    result = subtract_quantities("100g", "150g")
    print(f"100g - 150g = {result}")
    
    # Edge Case 2: Exact consumption
    print("\n2. Exact consumption:")
    result = subtract_quantities("200g", "200g")
    print(f"200g - 200g = {result}")
    
    # Edge Case 3: Different units (should handle gracefully)
    print("\n3. Different units:")
    result = subtract_quantities("2 cups", "100g")
    print(f"2 cups - 100g = {result}")
    
    # Edge Case 4: Invalid/malformed quantities
    print("\n4. Invalid quantities:")
    try:
        amount, unit = parse_quantity("invalid")
        print(f"'invalid' -> {amount} {unit}")
    except:
        print("'invalid' -> Error handled")
    
    # Edge Case 5: Zero quantities
    print("\n5. Zero quantities:")
    result = subtract_quantities("0g", "50g")
    print(f"0g - 50g = {result}")
    
    # Edge Case 6: Ingredient not in inventory
    print("\n6. Ingredient not in original inventory:")
    inventory = ["chicken: 300g"]
    used = [{"name": "beef", "quantity": "100g"}]
    updates = calculate_inventory_updates(inventory, used)
    print(f"Used beef (not in inventory): {updates}")
    
    # Edge Case 7: Empty inventory
    print("\n7. Empty inventory:")
    inventory = []
    used = [{"name": "chicken", "quantity": "100g"}]
    updates = calculate_inventory_updates(inventory, used)
    print(f"Empty inventory with usage: {updates}")
    
    # Edge Case 8: No ingredients used
    print("\n8. No ingredients used:")
    inventory = ["chicken: 300g", "rice: 2 cups"]
    used = []
    updates = calculate_inventory_updates(inventory, used)
    print(f"No usage: {updates}")

def test_api_edge_cases():
    print("\n=== TESTING API EDGE CASES ===")
    
    import requests
    import json
    
    base_url = "http://127.0.0.1:8087/generate-meal-plan"
    
    # Edge Case 1: Very low inventory
    print("\n1. Very low inventory:")
    try:
        response = requests.post(base_url, json={
            "goals": {"calories": 2000, "protein": 100},
            "inventory": ["chicken: 50g", "rice: 0.1 cups"]
        }, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Remaining: {data.get('inventory_updates', {}).get('remaining', 'N/A')}")
        else:
            print(f"API Error: {response.status_code}")
    except Exception as e:
        print(f"Request failed: {e}")
    
    # Edge Case 2: Empty inventory
    print("\n2. Empty inventory:")
    try:
        response = requests.post(base_url, json={
            "goals": {"calories": 1000, "protein": 50},
            "inventory": []
        }, timeout=10)
        print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_edge_cases()
    test_api_edge_cases()
    print("\n✅ Edge case testing completed!")
