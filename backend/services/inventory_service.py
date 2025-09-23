# Implement inventory_service.py for adding/updating inventory

import os
from typing import Optional
from backend.models import InventoryItem, InventoryList
from backend.storage.repo import read_json, write_json

# Path to inventory storage file (you can adjust path if needed)
INVENTORY_FILE = os.path.join("backend", "storage", "inventory.json")

def load_inventory() -> InventoryList:
    """Load inventory from JSON file, return as InventoryList model"""
    try:
        data = read_json(INVENTORY_FILE)
        return InventoryList(items=[InventoryItem(**item) for item in data])
    except FileNotFoundError:
        return InventoryList(items=[])

def save_inventory(inventory: InventoryList) -> None:
    """Save InventoryList to JSON file"""
    write_json(INVENTORY_FILE, [item.dict() for item in inventory.items])

def add_or_update_item(name: str, quantity: int, unit: str) -> InventoryItem:
    inventory = load_inventory()

    for item in inventory.items:
        if item.name.lower() == name.lower() and item.unit == unit:
            item.quantity += quantity
            save_inventory(inventory)
            return item

    # if not found, create new
    new_item = InventoryItem(name=name, quantity=quantity, unit=unit)
    inventory.items.append(new_item)
    save_inventory(inventory)
    return new_item

def get_inventory() -> InventoryList:
    """Return the full inventory list"""
    return load_inventory()
