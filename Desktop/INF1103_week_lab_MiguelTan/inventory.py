from physical_product import PhysicalProduct
from digital_product import DigitalProduct

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def search_product(self, product_id):
        for product in self.products:
            if product.get_id() == product_id:
                return product
        return None

    def display_all(self):
        print("Current Inventory:")
        for product in self.products:
            product.display_information()

    
if __name__ == "__main__":
    inventory = Inventory()

    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5)
    mouse = DigitalProduct("P002", "Photoshop", 25.50, 40, 100)

    inventory.add_product(laptop)
    inventory.add_product(mouse)

    inventory.display_all()

    found = inventory.search_product("P001")

    if found:
        print("Product found!")
        found.display_information()