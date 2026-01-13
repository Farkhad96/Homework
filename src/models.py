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

    def __add__(self, other: "Product") -> Union[float, Decimal]:
        """Add total prices of two Product instances.
        Args:
            other: Another Product instance
        Returns:
            Sum of total prices (price * quantity) of both products
        """
        if type(self) is not type(other):
            raise TypeError("Both products must be of the same type to add their total prices.")
        if not isinstance(other, Product):
            return NotImplemented
        total_price = self.__price * self.quantity + other.__price * other.quantity
        return total_price

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

    def __str__(self):
        return f"{self.name},{self.price} руб.,{self.quantity} шт."

    @price.setter
    def price(self, new_price: Union[float, Decimal]) -> None:
        """Set the product price, ensuring it is non-negative.

        Args:
            new_price: New price to set (float or Decimal)
        """
        if new_price < self.__price:
            if (
                input(f"New price {new_price} is lower than current price {self.__price}. Are you sure? (y/n): ")
                == "y"
            ):
                self.__price = new_price
                if new_price < 0:
                    self.__price = 0
        else:
            self.__price = new_price
            if new_price < 0:
                self.__price = 0


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: Union[float, Decimal],
        quantity: int,
        efficiency: str,
        model: str,
        memory: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: Union[float, Decimal],
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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
        if not isinstance(product, Product):
            raise TypeError("Only Product instances can be added to the category.")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List["Product"]:
        """Get the list of products in the category."""
        return self.__products

    def __str__(self):
        quantity_in_category = 0
        for product in self.__products:
            quantity_in_category += product.quantity
        return f"{self.name}, количество продуктов {quantity_in_category} шт."


class ProductsInCategory:
    def __init__(self, category: Category):
        self.name = category.name
        self.description = category.description
        self.__products = category.products

    def __iter__(self):
        """Initialize iterator over products in the category."""
        self.current = 0
        return self

    def __next__(self):
        """Iterate over products in the category."""
        if self.current < len(self.__products):
            product = self.__products[self.current]
            self.current += 1
            return product
        else:
            raise StopIteration

    @staticmethod
    def get_products_in_category(category: Category) -> List[Product]:
        """Get products in a given category.

        Args:
            category: Category object

        Returns:
            List of Product objects in the category
        """
        return category.products
