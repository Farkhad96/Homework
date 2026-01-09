"""Product and Category models."""
from decimal import Decimal
from typing import Union
import json


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
    
    def __init__(self, name: str, description: str, products: list):
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


def load_from_json(path: str) -> list:
    """Load categories from JSON file.
    
    Args:
        path: Path to JSON file
        
    Returns:
        List of Category objects
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    categories = []
    for category_data in data:
        products = []
        for product_data in category_data.get('products', []):
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            products.append(product)
        
        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)
    
    return categories
