# Testing backend/storage/repo.py

import os
import tempfile
from backend.storage import repo


def test_write_and_read_json():
    # Create a temporary file to simulate storage
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        test_path = tmp_file.name

    try:
        # Test data
        data = [
            {"id": 1, "name": "Chicken", "quantity": 5},
            {"id": 2, "name": "Tuna", "quantity": 3},
        ]

        # Write data to temp file
        repo.write_json(test_path, data)

        # Read back data
        loaded = repo.read_json(test_path)

        assert loaded == data  # ✅ round-trip works

    finally:
        # Cleanup temp file
        os.remove(test_path)


def test_read_nonexistent_file_returns_empty_list():
    # A random path that doesn’t exist
    fake_path = "does_not_exist.json"

    result = repo.read_json(fake_path)

    assert result == []  # ✅ default behavior

if __name__ == "__main__":
    test_write_and_read_json()
    test_read_nonexistent_file_returns_empty_list()
    print("All tests passed ✅")

