# Testing backend/services/inventory_service.py

import os
from backend.services.inventory_service import add_or_update_item, get_inventory, save_inventory
from backend.models import InventoryList

# Path to inventory file (same as in inventory_service.py)
INVENTORY_FILE = os.path.join("test", "test_inventory.json")

def reset_inventory():
    save_inventory(InventoryList(items=[]))

def test_add_item():
    reset_inventory()
    item = add_or_update_item("Apple", 5, "pcs")
    assert item.name == "Apple"
    assert item.quantity == 5
    assert item.unit == "pcs"
    print("✅ test_add_item passed")

def test_update_item():
    reset_inventory()
    add_or_update_item("Banana", 3, "pcs")
    item = add_or_update_item("Banana", 2, "pcs")  # should update
    assert item.quantity == 5
    print("✅ test_update_item passed")

def test_get_inventory():
    reset_inventory()
    add_or_update_item("Orange", 4, "pcs")
    inventory = get_inventory()
    assert len(inventory.items) == 1
    assert inventory.items[0].name == "Orange"
    assert inventory.items[0].quantity == 4
    assert inventory.items[0].unit == "pcs"
    print("✅ test_get_inventory passed")

if __name__ == "__main__":
    test_add_item()
    test_update_item()
    test_get_inventory()
    print("🎉 All inventory_service tests passed")

    # 🧹 Cleanup: delete the JSON file (comment this out if you want to inspect the file)
    if os.path.exists(INVENTORY_FILE):
        os.remove(INVENTORY_FILE)
        print(f"🗑️ Cleaned up test file: {INVENTORY_FILE}")
