from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.supplier: Supplier = supplier

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def update_stock(self, quantity: int) -> None:
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id}, Name: {self.__name}, Price: ${self.__price:.2f}, Stock: {self.__stock}")

    def get_id(self) -> str:
        return self.__product_id


    @property
    def price(self) -> float:
        return self.__price

    def to_dict(self) -> dict[str, str | float | int | dict[str, str]]:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.supplier.to_dict()
        }
