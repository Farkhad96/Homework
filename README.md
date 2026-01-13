# Homework - Product and Category Classes

This project implements Product and Category classes with automatic counting functionality and JSON loading capabilities.

## Features

### Product Class
- **Attributes:**
  - `name` (str): Product name
  - `description` (str): Product description
  - `price` (float/Decimal): Product price
  - `quantity` (int): Product quantity in stock
- **Class attributes:**
  - `list_of_products` (`list[Product]`): Tracks created products (used by `new_product`)
- **Behavior:**
  - `price` setter: prevents silently decreasing price (asks confirmation via `input()`); negative price is clamped to `0`
  - `__str__`: `"name,price руб.,quantity шт."`
  - `__add__(other)`: returns combined total value: `self.price*self.quantity + other.price*other.quantity`
    - only allowed for the *same concrete class* (e.g., `Smartphone + Smartphone`)

### Specialized Products
- **Smartphone(Product)** adds:
  - `efficiency`, `model`, `memory`, `color`
- **LawnGrass(Product)** adds:
  - `country`, `germination_period`, `color`

### Category Class
- **Instance attributes:**
  - `name` (str): Category name
  - `description` (str): Category description
  - `products` (`list[Product]`): List of Product objects (stored internally as a private list)
- **Class attributes (counters):**
  - `category_count`: incremented when a new `Category` is created
  - `product_count`: incremented by `len(products)` when a new `Category` is created
    - Note: this counter tracks the number of `Product` *objects*, not `quantity` totals
- **Methods:**
  - `add_product(product: Product)`: appends product to the category
    - validates type (`Product` only)
    - increments `Category.product_count` by `1` (per current implementation)
- **`__str__`:**
  - shows total *quantity* across products, e.g. `"Electronics, количество продуктов 5 шт."`

### Iteration over Category Products
- `ProductsInCategory(category)` provides an iterator over `category.products`
- Also includes `get_products_in_category(category) -> list[Product]`

### Functions
- `load_from_json(path: str) -> list[Category]`: loads categories and products from a JSON file

## Quick Start

```bash
pip install -r requirements.txt
pytest -q
```

Minimal run:

```bash
python main.py
```

## Project Structure

- `src/models.py` — core domain models (`Product`, `Category`, specialized products, iterator)
- `src/utils.py` — helpers (JSON loading)
- `tests/` — pytest suite
- `main.py` — example script / manual run

## API Cheatsheet (most used)

### Product
- `Product(name, description, price, quantity)`
- `Product.new_product(data: dict) -> Product`
- `product.price = new_price` (may prompt on decrease)
- `str(product)` → `"Name,price руб.,quantity шт."`
- `product1 + product2` → total inventory value (same concrete class only)

### Category
- `Category(name, description, products: list[Product])`
- `Category.category_count`, `Category.product_count`
- `category.add_product(product)`
- `category.products` (list-like)
- `str(category)` → total *quantity* across items in category

### Iteration
- `for p in ProductsInCategory(category): ...`
- `ProductsInCategory.get_products_in_category(category) -> list[Product]`

## Important Notes / Edge Cases

### Price setter behavior
- If you set a **lower** price, the setter asks for confirmation via `input()`.
- Any negative price is **clamped to `0`**.

### `Product.__add__` rules
- Only supported when both operands are the **same concrete class**:
  - OK: `Product + Product`, `Smartphone + Smartphone`
  - Error: `Smartphone + Product` (raises `TypeError`)
- The result is a number: `(price * quantity) + (other.price * other.quantity)`.

### Counters (`Category.category_count`, `Category.product_count`)
- `category_count` increments per created `Category`.
- `product_count` counts **Product objects**, not quantities in stock.
- `Category.__str__` prints **sum of quantities** across all products.

### JSON loading (`load_from_json`)
- Validates presence of required fields for categories and products.
- Raises:
  - `FileNotFoundError` if path is missing
  - `json.JSONDecodeError` if malformed JSON
  - `KeyError` if required fields are absent

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
print(Category.product_count)   # 2  (counts Product objects)
```

### Creating Specialized Products

```python
from src.models import Smartphone, LawnGrass

phone = Smartphone("Phone", "Flagship", 799.99, 5, "High", "ModelZ", "512GB", "Blue")
grass = LawnGrass("Grass", "Premium", 29.99, 50, "USA", "7-14 days", "Green")
```

### Summing Inventory Value (`Product.__add__`)

```python
from src.models import Product

p1 = Product("A", "Desc", 10.0, 5)   # total 50
p2 = Product("B", "Desc", 20.0, 3)   # total 60

print(p1 + p2)  # 110.0
```

> Note: addition requires both operands to be the same concrete class (e.g., `Smartphone + Smartphone`).

### Creating Products from Dictionaries (`Product.new_product`)

```python
from src.models import Product

p = Product.new_product({
    "name": "Keyboard",
    "description": "Mechanical",
    "price": 100.0,
    "quantity": 2
})
```

`new_product` validates required fields and types. If a product with the same name already exists in `Product.list_of_products`, quantity is combined and price may be kept at the higher value.

### Iterating over products in a category

```python
from src.models import Category, Product, ProductsInCategory

cat = Category("Cat", "Desc", [Product("P", "D", 10.0, 1)])

for product in ProductsInCategory(cat):
    print(product.name)
```

### Loading from JSON

```python
from src.utils import load_from_json

categories = load_from_json("products.json")
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
pytest -q
```

## Development Tips

- If tests fail due to interactive prompts, use `pytest` (the suite already monkeypatches `input()` where needed).
- Keep an eye on `Product.list_of_products` during tests: it’s global state and is reset in the test setup.

## Test Coverage

The test suite includes:
- Product initialization with float and Decimal prices
- Product string formatting, addition rules, and price setter confirmation behavior
- Category initialization and counters (`category_count`, `product_count`)
- Loading data from JSON files and error cases
- Specialized products (`Smartphone`, `LawnGrass`)
- Iteration over products in a category
