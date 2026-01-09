# Homework - Product and Category Classes

This project implements Product and Category classes with automatic counting functionality and JSON loading capabilities.

## Features

### Product Class
- **Attributes:**
  - `name` (str): Product name
  - `description` (str): Product description
  - `price` (float/Decimal): Product price
  - `quantity` (int): Product quantity in stock

### Category Class
- **Instance Attributes:**
  - `name` (str): Category name
  - `description` (str): Category description
  - `products` (list[Product]): List of Product objects

- **Class Attributes:**
  - `category_count`: Automatically incremented when a new Category is created
  - `product_count`: Automatically incremented by the number of products when a new Category is created

### Functions
- `load_from_json(path: str) -> list[Category]`: Loads categories and products from a JSON file

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Creating Products and Categories

```python
from src.models import Product, Category

# Create products
laptop = Product("Laptop", "High-performance laptop", 999.99, 10)
mouse = Product("Mouse", "Wireless mouse", 25.50, 50)

# Create category
electronics = Category(
    "Electronics",
    "Electronic devices and accessories",
    [laptop, mouse]
)

# Check counters
print(Category.category_count)  # 1
print(Category.product_count)   # 2
```

### Loading from JSON

```python
from src.models import load_from_json

categories = load_from_json('products.json')
for category in categories:
    print(f"{category.name}: {len(category.products)} products")
```

### JSON Format

The `products.json` file should follow this structure:

```json
[
  {
    "name": "Category Name",
    "description": "Category Description",
    "products": [
      {
        "name": "Product Name",
        "description": "Product Description",
        "price": 99.99,
        "quantity": 10
      }
    ]
  }
]
```

## Running Tests

```bash
pytest tests/test_models.py -v
```

## Example

Run the example script to see the classes in action:

```bash
python3 example.py
```

## Test Coverage

The test suite includes:
- Product initialization with float and Decimal prices
- Category initialization
- Correct incrementation of `category_count`
- Correct incrementation of `product_count`
- Loading data from JSON files
- Edge cases (empty product lists)