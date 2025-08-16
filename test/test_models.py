# backend/test_models.py
from backend.models import InventoryItem, InventoryList
from pydantic import ValidationError

def run_tests():
    # ✅ Valid item
    egg = InventoryItem(
        name="Egg",
        quantity=12,
        unit="pieces",
        calories=70,
        protein=6
    )
    print("Valid Item Created:")
    print(egg.json(indent=2))  # Pretty print JSON

    # ✅ Valid list
    inventory = InventoryList(items=[egg])
    print("\nInventory List:")
    print(inventory.json(indent=2))

    # ❌ Invalid item (wrong type for quantity)
    try:
        bad_item = InventoryItem(
            name="Milk",
            quantity="two liters",  # invalid type
            unit="liters"
        )
    except ValidationError as e:
        print("\nValidation Error Example:")
        print(e)

if __name__ == "__main__":
    run_tests()
