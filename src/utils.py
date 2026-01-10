import json
from typing import List

from src.models import Category, Product


def load_from_json(path: str) -> List[Category]:
    """Load categories from JSON file.

    Args:
        path: Path to JSON file

    Returns:
        List of Category objects

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the JSON is malformed
        KeyError: If required fields are missing in JSON data
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON format in {path}: {e.msg}", e.doc, e.pos)

    categories = []
    for category_data in data:
        try:
            products = []
            for product_data in category_data.get("products", []):
                # Validate required fields
                required_fields = ["name", "description", "price", "quantity"]
                missing_fields = [field for field in required_fields if field not in product_data]
                if missing_fields:
                    raise KeyError(f"Missing required fields in product data: {missing_fields}")

                product = Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    quantity=product_data["quantity"],
                )
                products.append(product)

            # Validate required fields for category
            required_fields = ["name", "description"]
            missing_fields = [field for field in required_fields if field not in category_data]
            if missing_fields:
                raise KeyError(f"Missing required fields in category data: {missing_fields}")

            category = Category(
                name=category_data["name"], description=category_data["description"], products=products
            )
            categories.append(category)
        except KeyError as e:
            raise KeyError(f"Error processing category data: {e}")

    return categories
