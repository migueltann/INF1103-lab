class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, quantity):
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id}, Name: {self.__name}, Price: ${self.__price:.2f}, Stock: {self.__stock}")


if __name__ == "__main__":
    laptop = Product("P001", "Laptop", 1200.00, 15)

    laptop.display_information()
    laptop.update_stock(20)
    laptop.display_information()