from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        # Calculate shipping cost using self.__weight
        shipping_cost = self.__weight * 5  # Example calculation: $5 per kg
        # Return the result
        return shipping_cost

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


    def display_information(self):
        super().display_information()
        print("Weight:", self.__weight, "kg")