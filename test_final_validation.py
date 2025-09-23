#!/usr/bin/env python3

import requests
import json

def test_comprehensive_scenarios():
    print("=== COMPREHENSIVE API VALIDATION ===")
    
    base_url = "http://127.0.0.1:8087/generate-meal-plan"
    
    scenarios = [
        {
            "name": "Happy Path",
            "data": {
                "goals": {"calories": 1500, "protein": 80},
                "inventory": ["chicken: 400g", "rice: 2 cups", "eggs: 6 pieces"]
            }
        },
        {
            "name": "Low Inventory (Potential Over-consumption)",
            "data": {
                "goals": {"calories": 2000, "protein": 100},
                "inventory": ["chicken: 50g", "rice: 0.2 cups"]
            }
        },
        {
            "name": "Malformed Inventory",
            "data": {
                "goals": {"calories": 1200, "protein": 60},
                "inventory": ["chicken", "rice: invalid", "eggs: ", "beef: 200g"]
            }
        },
        {
            "name": "Empty Inventory",
            "data": {
                "goals": {"calories": 1000, "protein": 50},
                "inventory": []
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        try:
            response = requests.post(base_url, json=scenario['data'], timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we have inventory updates
                if 'inventory_updates' in data:
                    updates = data['inventory_updates']
                    print(f"✅ Status: Success")
                    print(f"📊 Before: {len(updates.get('before', {}))} items")
                    print(f"🍽️ Used: {len(updates.get('used', {}))} items")
                    print(f"📦 Remaining: {len(updates.get('remaining', {}))} items")
                    
                    # Check for warnings
                    warnings = updates.get('warnings', [])
                    if warnings:
                        print(f"⚠️ Warnings ({len(warnings)}):")
                        for warning in warnings[:3]:  # Show first 3
                            print(f"   - {warning}")
                    else:
                        print("✅ No warnings")
                        
                    # Check for error conditions in remaining
                    remaining = updates.get('remaining', {})
                    error_count = sum(1 for v in remaining.values() 
                                    if any(keyword in str(v) for keyword in 
                                          ['INSUFFICIENT', 'INVALID', 'UNIT_MISMATCH']))
                    if error_count > 0:
                        print(f"🚨 {error_count} items with issues")
                else:
                    print("❌ No inventory updates in response")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n=== VALIDATION COMPLETE ===")

if __name__ == "__main__":
    test_comprehensive_scenarios()
