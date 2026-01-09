"""Product and Category models."""

import json
from decimal import Decimal
from typing import List, Union


class Product:
    """Product class with name, description, price, and quantity."""

    def __init__(self, name: str, description: str, price: Union[float, Decimal], quantity: int):
        """Initialize Product with all fields.

        Args:
            name: Product name
            description: Product description
            price: Product price (float or Decimal)
            quantity: Product quantity
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Category class with name, description, and list of products."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List["Product"]):
        """Initialize Category with all fields and update class counters.

        Args:
            name: Category name
            description: Category description
            products: List of Product objects
        """
        self.name = name
        self.description = description
        self.products = products

        # Update class attributes
        Category.category_count += 1
        Category.product_count += len(products)


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
