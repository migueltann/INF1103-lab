from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Order quantity must be positive.")
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, index: int) -> None:
        del self.__order_lines[index]

    def calculate_total(self) -> float:
        return sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)
