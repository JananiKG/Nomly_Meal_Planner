import re
from typing import Tuple, Dict, List


def parse_quantity(quantity_str: str) -> Tuple[float, str]:
    """
    Parse quantity string like '150g', '2 cups', '3 pieces' into (amount, unit)
    Returns: (float_amount, unit_string)
    """
    if not quantity_str or not quantity_str.strip():
        return 0.0, ""
    
    quantity_str = quantity_str.strip()
    
    # Handle fractions like "1/2 cup"
    if "/" in quantity_str:
        parts = quantity_str.split()
        if len(parts) >= 2:
            fraction_part = parts[0]
            unit_part = " ".join(parts[1:])
            if "/" in fraction_part:
                try:
                    num, denom = fraction_part.split("/")
                    amount = float(num) / float(denom)
                    return amount, unit_part
                except (ValueError, ZeroDivisionError):
                    return 0.0, quantity_str
    
    # Extract number and unit using regex
    match = re.match(r'([\d\.]+)\s*(.+)', quantity_str)
    if match:
        try:
            amount = float(match.group(1))
            unit = match.group(2).strip()
            return amount, unit
        except ValueError:
            return 0.0, quantity_str
    
    # Try to extract just a number
    number_match = re.match(r'^([\d\.]+)$', quantity_str)
    if number_match:
        try:
            return float(number_match.group(1)), ""
        except ValueError:
            pass
    
    # Invalid format
    return 0.0, quantity_str


def subtract_quantities(available: str, used: str) -> str:
    """
    Subtract used quantity from available quantity with proper error handling
    Returns: remaining quantity as string with units or error message
    """
    avail_amount, avail_unit = parse_quantity(available)
    used_amount, used_unit = parse_quantity(used)
    
    # Handle invalid quantities
    if avail_amount == 0.0 and avail_unit == available:
        return f"INVALID_QUANTITY: {available}"
    
    if used_amount == 0.0 and used_unit == used:
        return f"INVALID_QUANTITY: {used}"
    
    # Normalize units for comparison (handle singular/plural)
    def normalize_unit(unit):
        unit = unit.lower().strip()
        # Handle common plural forms
        if unit.endswith('s') and len(unit) > 1:
            return unit[:-1]  # Remove 's' from plural
        return unit
    
    avail_unit_norm = normalize_unit(avail_unit)
    used_unit_norm = normalize_unit(used_unit)
    
    # Unit mismatch handling (only if both units exist and are different)
    if (avail_unit_norm != used_unit_norm and 
        avail_unit and used_unit and 
        avail_unit_norm and used_unit_norm):
        return f"UNIT_MISMATCH: {available} vs {used}"
    
    # Use the available unit as reference
    unit = avail_unit if avail_unit else used_unit
    
    remaining = avail_amount - used_amount
    
    # Handle over-consumption
    if remaining < 0:
        return f"INSUFFICIENT: Need {used_amount} {unit}, have {avail_amount} {unit}"
    
    if remaining == 0:
        return f"0 {unit}"
    
    return f"{remaining} {unit}"


def parse_inventory_list(inventory: List[str]) -> Dict[str, str]:
    """
    Parse inventory list like ['chicken: 300g', 'rice: 2 cups'] 
    into dict {'chicken': '300g', 'rice': '2 cups'}
    Handles malformed entries gracefully
    """
    result = {}
    for item in inventory:
        if ":" in item:
            name, quantity = item.split(":", 1)
            name = name.strip().lower()
            quantity = quantity.strip()
            
            # Validate quantity format
            amount, unit = parse_quantity(quantity)
            if amount == 0.0 and unit == quantity and quantity:
                # Invalid quantity format
                result[name] = f"INVALID: {quantity}"
            else:
                result[name] = quantity
        else:
            # No colon separator - treat as invalid
            result[item.strip().lower()] = "MISSING_QUANTITY"
    return result


def calculate_inventory_updates(original_inventory: List[str], used_ingredients: List[Dict]) -> Dict:
    """
    Calculate inventory updates based on used ingredients with comprehensive error handling
    Returns: dict with before, used, remaining, and warnings
    """
    inventory_dict = parse_inventory_list(original_inventory)
    used_dict = {}
    remaining_dict = {}
    warnings = []
    
    # Calculate used amounts
    for ingredient in used_ingredients:
        name = ingredient.get("name", "").lower()
        quantity = ingredient.get("quantity", "0")
        if name:
            used_dict[name] = quantity
    
    # Calculate remaining amounts and detect issues
    for name, available_qty in inventory_dict.items():
        if name in used_dict:
            remaining_qty = subtract_quantities(available_qty, used_dict[name])
            remaining_dict[name] = remaining_qty
            
            # Check for warnings
            if remaining_qty.startswith("INSUFFICIENT"):
                warnings.append(f"Over-consumed {name}: {remaining_qty}")
            elif remaining_qty.startswith("UNIT_MISMATCH"):
                warnings.append(f"Unit mismatch for {name}: {remaining_qty}")
            elif remaining_qty.startswith("INVALID_QUANTITY"):
                warnings.append(f"Invalid quantity for {name}: {remaining_qty}")
        else:
            remaining_dict[name] = available_qty
            if available_qty.startswith("INVALID"):
                warnings.append(f"Invalid inventory entry: {name} = {available_qty}")
    
    # Check for ingredients used but not in inventory
    for name in used_dict:
        if name not in inventory_dict:
            warnings.append(f"Used ingredient not in inventory: {name}")
    
    result = {
        "before": inventory_dict,
        "used": used_dict,
        "remaining": remaining_dict
    }
    
    if warnings:
        result["warnings"] = warnings
    
    return result
