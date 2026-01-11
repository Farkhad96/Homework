"""Example usage of Product and Category classes."""

import os
import sys

from src.models import Category, Product
from src.utils import load_from_json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def main():
    """Demonstrate Product and Category functionality."""
    print("=== Product and Category Example ===\n")

    # Reset counters for demo
    Category.category_count = 0
    Category.product_count = 0

    # Create products
    print("Creating products...")
    laptop = Product("Laptop", "High-performance laptop", 999.99, 10)
    mouse = Product("Mouse", "Wireless mouse", 25.50, 50)
    keyboard = Product("Keyboard", "Mechanical keyboard", 89.99, 30)

    print(f"  - {laptop.name}: ${laptop.price}, quantity: {laptop.quantity}")
    print(f"  - {mouse.name}: ${mouse.price}, quantity: {mouse.quantity}")
    print(f"  - {keyboard.name}: ${keyboard.price}, quantity: {keyboard.quantity}")

    # Create categories
    print("\nCreating categories...")
    electronics = Category("Electronics", "Electronic devices and accessories", [laptop, mouse, keyboard])
    print(f"  - {electronics.name}: {len(electronics.products)} products")

    book1 = Product("Python Programming", "Learn Python from scratch", 39.99, 20)
    book2 = Product("Data Science", "Introduction to Data Science", 49.99, 15)

    books = Category("Books", "Programming and technical books", [book1, book2])
    print(f"- {books.name}: {len(books.products)} products")

    # Display counters
    print("\n=== Counters ===")
    print(f"Total categories: {Category.category_count}")
    print(f"Total products: {Category.product_count}")

    # Load from JSON
    print("\n=== Loading from JSON ===")
    Category.category_count = 0
    Category.product_count = 0

    json_path = os.path.join(os.path.dirname(__file__), "products.json")
    if os.path.exists(json_path):
        categories = load_from_json(json_path)
        print(f"Loaded {len(categories)} categories from products.json")

        for cat in categories:
            print(f"\n{cat.name}:")
            for prod in cat.products:
                print(f"- {prod.name}: ${prod.price}, qty: {prod.quantity}")

        print("\n=== Counters after loading ===")
        print(f"Total categories: {Category.category_count}")
        print(f"Total products: {Category.product_count}")
    else:
        print("products.json not found")


if __name__ == "__main__":
    main()
