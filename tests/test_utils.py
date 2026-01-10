import json
import os
import sys

import pytest

from src.models import Category, Product
from src.utils import load_from_json

# Add project root to path (so `import src...` works)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestLoadFromJson:
    """Tests for load_from_json function."""

    def setup_method(self):
        """Reset class attributes before each test."""
        Category.category_count = 0
        Category.product_count = 0
        Product.list_of_products = []

    def test_load_from_json(self, tmp_path):
        """Test loading categories from JSON file."""
        # Create temporary JSON file
        json_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices",
                "products": [
                    {"name": "Laptop", "description": "High-performance laptop", "price": 999.99, "quantity": 10},
                    {"name": "Mouse", "description": "Wireless mouse", "price": 25.50, "quantity": 50},
                ],
            },
            {
                "name": "Books",
                "description": "Various books",
                "products": [
                    {"name": "Python Programming", "description": "Learn Python", "price": 39.99, "quantity": 20}
                ],
            },
        ]

        json_file = tmp_path / "test_products.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f)

        # Load categories
        categories = load_from_json(str(json_file))

        # Verify results
        assert len(categories) == 2
        assert Category.category_count == 2
        # product_count increments by number of Product objects created (2 + 1)
        assert Category.product_count == 3

        # Check first category
        assert categories[0].name == "Electronics"
        assert categories[0].description == "Electronic devices"
        assert len(categories[0].products) == 2
        assert categories[0].products[0].name == "Laptop"
        assert categories[0].products[0].price == 999.99
        assert categories[0].products[1].name == "Mouse"

        # Check second category
        assert categories[1].name == "Books"
        assert len(categories[1].products) == 1
        assert categories[1].products[0].name == "Python Programming"

    def test_load_from_existing_products_json(self):
        """Test loading from the actual products.json file."""
        # Get the path to products.json in the repository
        json_path = os.path.join(os.path.dirname(__file__), "..", "products.json")

        if os.path.exists(json_path):
            categories = load_from_json(json_path)

            assert len(categories) > 0
            assert Category.category_count > 0
            assert Category.product_count > 0

            # Verify each category has required attributes
            for category in categories:
                assert hasattr(category, "name")
                assert hasattr(category, "description")
                assert hasattr(category, "products")
                assert isinstance(category.products, list)

                # Verify each product has required attributes
                for product in category.products:
                    assert hasattr(product, "name")
                    assert hasattr(product, "description")
                    assert hasattr(product, "price")
                    assert hasattr(product, "quantity")

    def test_load_from_json_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(FileNotFoundError):
            load_from_json("/nonexistent/path/file.json")

    def test_load_from_json_invalid_json(self, tmp_path):
        """Test that JSONDecodeError is raised for invalid JSON."""
        json_file = tmp_path / "invalid.json"
        with open(json_file, "w") as f:
            f.write("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            load_from_json(str(json_file))

    def test_load_from_json_missing_product_fields(self, tmp_path):
        """Test that KeyError is raised when product fields are missing."""
        json_data = [
            {
                "name": "Test Category",
                "description": "Test",
                "products": [
                    {
                        "name": "Product",
                        # Missing description, price, quantity
                    }
                ],
            }
        ]

        json_file = tmp_path / "incomplete.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f)

        with pytest.raises(KeyError):
            load_from_json(str(json_file))
