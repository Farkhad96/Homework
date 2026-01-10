"""Product and Category models."""

from decimal import Decimal
from typing import List, Union


class Product:
    """Product class with name, description, price, and quantity."""

    list_of_products: List["Product"] = []

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
        self.__price = price
        self.quantity = quantity
        Product.list_of_products.append(self)

    @classmethod
    def new_product(cls, data: dict) -> "Product":
        """Create a new Product instance from a dictionary.

        Args:
            data: Dictionary with product fields (name, description, price, quantity)
        Returns:
            Product instance
        Raises:
            ValueError: If required fields are missing
            TypeError: If price or quantity types are incorrect
        """
        if not all(key in data for key in ("name", "description", "price", "quantity")):
            raise ValueError("Missing required product fields in data dictionary")
        if not isinstance(data["price"], (float, Decimal)):
            raise TypeError("Price must be a float or Decimal")
        if not isinstance(data["quantity"], int):
            raise TypeError("Quantity must be an integer")
        for existing_product in Product.list_of_products:
            if existing_product.name == data["name"]:
                data["quantity"] += existing_product.quantity
                if existing_product.price > data["price"]:
                    data["price"] = existing_product.price
        else:
            Product.list_of_products.append(cls(data["name"], data["description"], data["price"], data["quantity"]))
            return cls(data["name"], data["description"], data["price"], data["quantity"])

    @property
    def price(self) -> Union[float, Decimal]:
        """Get the product price."""
        return self.__price

    @price.setter
    def price(self, new_price: Union[float, Decimal]) -> None:
        """Set the product price, ensuring it is non-negative.

        Args:
            new_price: New price to set (float or Decimal)
        """
        if new_price < self.__price:
            if input("New price is lower than current price. Are you sure? (y/n): ") != "y":
                if new_price < 0:
                    self.__price = 0
                else:
                    self.__price = new_price


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
        self.__products = products

        # Update class attributes
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: "Product") -> None:
        """Add a product to the category and update product count.

        Args:
            product: Product object to add
        """
        self.__products.append(product)
        Category.product_count += product.quantity

    @property
    def products(self) -> List["Product"]:
        """Get the list of products in the category.

        Returns:
            List of Product objects
        """
        return self.__products
