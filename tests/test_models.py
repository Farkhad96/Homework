"""Tests for Product and Category classes."""
import pytest
from decimal import Decimal
import json
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Product, Category, load_from_json


class TestProduct:
    """Tests for Product class."""
    
    def test_product_init_with_float_price(self):
        """Test Product initialization with float price."""
        product = Product(
            name="Laptop",
            description="High-performance laptop",
            price=999.99,
            quantity=10
        )
        
        assert product.name == "Laptop"
        assert product.description == "High-performance laptop"
        assert product.price == 999.99
        assert product.quantity == 10
    
    def test_product_init_with_decimal_price(self):
        """Test Product initialization with Decimal price."""
        product = Product(
            name="Mouse",
            description="Wireless mouse",
            price=Decimal("25.50"),
            quantity=50
        )
        
        assert product.name == "Mouse"
        assert product.description == "Wireless mouse"
        assert product.price == Decimal("25.50")
        assert product.quantity == 50


class TestCategory:
    """Tests for Category class."""
    
    def setup_method(self):
        """Reset class attributes before each test."""
        Category.category_count = 0
        Category.product_count = 0
    
    def test_category_init(self):
        """Test Category initialization."""
        products = [
            Product("Product1", "Description1", 10.0, 5),
            Product("Product2", "Description2", 20.0, 3)
        ]
        
        category = Category(
            name="Electronics",
            description="Electronic devices",
            products=products
        )
        
        assert category.name == "Electronics"
        assert category.description == "Electronic devices"
        assert category.products == products
        assert len(category.products) == 2
    
    def test_category_count_increment(self):
        """Test that category_count increments correctly."""
        initial_count = Category.category_count
        
        products1 = [Product("Product1", "Desc1", 10.0, 5)]
        category1 = Category("Cat1", "Description1", products1)
        
        assert Category.category_count == initial_count + 1
        
        products2 = [Product("Product2", "Desc2", 20.0, 3)]
        category2 = Category("Cat2", "Description2", products2)
        
        assert Category.category_count == initial_count + 2
    
    def test_product_count_increment(self):
        """Test that product_count increments correctly."""
        initial_count = Category.product_count
        
        products1 = [
            Product("Product1", "Desc1", 10.0, 5),
            Product("Product2", "Desc2", 20.0, 3)
        ]
        category1 = Category("Cat1", "Description1", products1)
        
        assert Category.product_count == initial_count + 2
        
        products2 = [
            Product("Product3", "Desc3", 30.0, 7),
            Product("Product4", "Desc4", 40.0, 2),
            Product("Product5", "Desc5", 50.0, 1)
        ]
        category2 = Category("Cat2", "Description2", products2)
        
        assert Category.product_count == initial_count + 5
    
    def test_category_with_empty_products(self):
        """Test Category with empty product list."""
        initial_cat_count = Category.category_count
        initial_prod_count = Category.product_count
        
        category = Category("Empty", "No products", [])
        
        assert Category.category_count == initial_cat_count + 1
        assert Category.product_count == initial_prod_count
        assert len(category.products) == 0


class TestLoadFromJson:
    """Tests for load_from_json function."""
    
    def setup_method(self):
        """Reset class attributes before each test."""
        Category.category_count = 0
        Category.product_count = 0
    
    def test_load_from_json(self, tmp_path):
        """Test loading categories from JSON file."""
        # Create temporary JSON file
        json_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices",
                "products": [
                    {
                        "name": "Laptop",
                        "description": "High-performance laptop",
                        "price": 999.99,
                        "quantity": 10
                    },
                    {
                        "name": "Mouse",
                        "description": "Wireless mouse",
                        "price": 25.50,
                        "quantity": 50
                    }
                ]
            },
            {
                "name": "Books",
                "description": "Various books",
                "products": [
                    {
                        "name": "Python Programming",
                        "description": "Learn Python",
                        "price": 39.99,
                        "quantity": 20
                    }
                ]
            }
        ]
        
        json_file = tmp_path / "test_products.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f)
        
        # Load categories
        categories = load_from_json(str(json_file))
        
        # Verify results
        assert len(categories) == 2
        assert Category.category_count == 2
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
        json_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'products.json'
        )
        
        if os.path.exists(json_path):
            categories = load_from_json(json_path)
            
            assert len(categories) > 0
            assert Category.category_count > 0
            assert Category.product_count > 0
            
            # Verify each category has required attributes
            for category in categories:
                assert hasattr(category, 'name')
                assert hasattr(category, 'description')
                assert hasattr(category, 'products')
                assert isinstance(category.products, list)
                
                # Verify each product has required attributes
                for product in category.products:
                    assert hasattr(product, 'name')
                    assert hasattr(product, 'description')
                    assert hasattr(product, 'price')
                    assert hasattr(product, 'quantity')
