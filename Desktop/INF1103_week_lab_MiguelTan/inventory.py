from product import Product


class Inventory:
    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_id: str) -> None:
        product = self.find_product(product_id)

        if product is not None:
            self.products.remove(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.get_id() == product_id:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def display_all(self) -> None:
        print("Current Inventory:")
        for product in self.products:
            product.display_information()


if __name__ == "__main__":
    from digital_product import DigitalProduct
    from physical_product import PhysicalProduct
    from supplier import Supplier

    inventory = Inventory()

    supplier = Supplier("S001", "Tech Supplier", "tech@example.com")

    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5, supplier)
    mouse = DigitalProduct("P002", "Photoshop", 25.50, 40, 100, supplier)

    inventory.add_product(laptop)
    inventory.add_product(mouse)

    inventory.display_all()

    found = inventory.search_product("P001")

    if found:
        print("Product found!")
        found.display_information()
