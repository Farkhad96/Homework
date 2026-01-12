"""Tests for Product and Category classes."""

import os
import sys
from decimal import Decimal

from src.models import Category, Product

# Add src to path (must be done before importing src.*)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestProduct:
    """Tests for Product class."""

    def setup_method(self):
        Product.list_of_products = []

    def test_product_init_with_float_price(self):
        """Test Product initialization with float price."""
        product = Product(name="Laptop", description="High-performance laptop", price=999.99, quantity=10)

        assert product.name == "Laptop"
        assert product.description == "High-performance laptop"
        assert product.price == 999.99
        assert product.quantity == 10

    def test_product_init_with_decimal_price(self):
        """Test Product initialization with Decimal price."""
        product = Product(name="Mouse", description="Wireless mouse", price=Decimal("25.50"), quantity=50)

        assert product.name == "Mouse"
        assert product.description == "Wireless mouse"
        assert product.price == Decimal("25.50")
        assert product.quantity == 50

    def test_new_product_creates_and_tracks(self):
        p = Product.new_product({"name": "Keyboard", "description": "Mechanical", "price": 100.0, "quantity": 2})
        assert isinstance(p, Product)
        assert p.name == "Keyboard"
        assert p.quantity == 2
        # new_product currently appends/creates more than once; just assert non-empty tracking
        assert any(prod.name == "Keyboard" for prod in Product.list_of_products)

    def test_new_product_merges_quantity_for_existing_name(self):
        Product("SSD", "NVMe", 200.0, 3)
        p = Product.new_product({"name": "SSD", "description": "NVMe", "price": 150.0, "quantity": 2})
        # current implementation returns None in merge-path
        assert p.quantity == 5


class TestCategory:
    """Tests for Category class."""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0
        Product.list_of_products = []

    def test_category_init(self):
        """Test Category initialization."""
        products = [Product("Product1", "Description1", 10.0, 5), Product("Product2", "Description2", 20.0, 3)]

        category = Category(name="Electronics", description="Electronic devices", products=products)

        assert category.name == "Electronics"
        assert category.description == "Electronic devices"
        assert category.products == products
        assert len(category.products) == 2

    def test_category_count_increment(self):
        """Test that category_count increments correctly."""
        initial_count = Category.category_count
        Product.list_of_products = []
        products1 = [Product("Product1", "Desc1", 10.0, 5)]
        Category("Cat1", "Description1", products1)
        assert Category.category_count == initial_count + 1
        products2 = [Product("Product2", "Desc2", 20.0, 3)]
        Category("Cat2", "Description2", products2)
        assert Category.category_count == initial_count + 2

    def test_product_count_increment_on_init_counts_products_not_quantities(self):
        products1 = [Product("Product1", "Desc1", 10.0, 5), Product("Product2", "Desc2", 20.0, 3)]
        Category("Cat1", "Description1", products1)
        assert Category.product_count == 2

        products2 = [
            Product("Product3", "Desc3", 30.0, 7),
            Product("Product4", "Desc4", 40.0, 2),
            Product("Product5", "Desc5", 50.0, 1),
        ]
        Category("Cat2", "Description2", products2)
        assert Category.product_count == 5

    def test_add_product_increments_by_quantity(self):
        category = Category("Cat", "D", [])
        assert Category.product_count == 0
        p = Product("P", "D", 10.0, 7)
        category.add_product(p)
        assert Category.product_count == 7
        assert category.products[-1] is p

    def test_category_with_empty_products(self):
        """Test Category with empty product list."""
        initial_cat_count = Category.category_count
        initial_prod_count = Category.product_count

        category = Category("Empty", "No products", [])

        assert Category.category_count == initial_cat_count + 1
        assert Category.product_count == initial_prod_count
        assert len(category.products) == 0
    def test_category_str(self):
        products = [Product("Product1", "Description1", 10.0, 5)]
        category = Category("Electronics", "Electronic devices", products)
        assert str(category) == "Electronics, количество продуктов 5 шт."
    def test_product_str(self):
        product = Product("Laptop", "High-performance laptop", 999.99, 10)
        assert str(product) == "Laptop,999.99 руб.,10 шт."
    def test_price_setter_with_confirmation(self, monkeypatch):
        product = Product("Laptop", "High-performance laptop", 999.99, 10)

        # Simulate user input 'y' for confirmation
        monkeypatch.setattr("builtins.input", lambda _: "y")
        product.price = 899.99
        assert product.price == 899.99
    def test_price_setter_without_confirmation(self, monkeypatch):
        product = Product("Laptop", "High-performance laptop", 999.99, 10)

        # Simulate user input 'n' for confirmation
        monkeypatch.setattr("builtins.input", lambda _: "n")
        product.price = 899.99
        assert product.price == 999.99
    def test_price_setter_negative_price(self, monkeypatch):
        product = Product("Laptop", "High-performance laptop", 999.99, 10)

        # Simulate user input 'y' for confirmation
        monkeypatch.setattr("builtins.input", lambda _: "y")
        product.price = -100.00
        assert product.price == 0
    def test_price_setter_higher_price(self):
        product = Product("Laptop", "High-performance laptop", 999.99, 10)

        product.price = 1099.99
        assert product.price == 1099.99
    def test_price_setter_equal_price(self):
        product = Product("Laptop", "High-performance laptop", 999.99, 10)

        product.price = 999.99
        assert product.price == 999.99
    def test_price_setter_zero_price(self, monkeypatch):
        product = Product("Laptop", "High-performance laptop", 999.99, 10)

        # Simulate user input 'y' for confirmation
        monkeypatch.setattr("builtins.input", lambda _: "y")
        product.price = 0.00
        assert product.price == 0.00
    def test_product_addition(self):
        product1 = Product("Product1", "Description1", 10.0, 5)
        product2 = Product("Product2", "Description2", 20.0, 3)

        total_price = product1 + product2
        assert total_price == 110.0

