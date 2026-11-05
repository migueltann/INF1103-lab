from product import Product

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)  # Reuse the parent's constructor
        self.__download_size = download_size  # Initialise the download_size attribute

    def get_fulfilment_info(self):
            return "This product is delivered digitally."

    def to_dict(self):
            data = super().to_dict()
            data["type"] = "digital"
            data["download_size"] = self.__download_size
            return data

    def display_information(self):
        super().display_information()  # Call the parent's display_information method
        print("Download Size:", self.__download_size, "MB")  # Display the download size