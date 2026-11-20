from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, *,
               weight: float | None = None,
               download_size: float | None = None) -> Product:
        if product_type == "physical":
            if weight is None or weight < 0:
                raise ValueError("Physical product requires a non-negative weight.")
            return PhysicalProduct(product_id, name, price, stock_quantity, weight, supplier)
        elif product_type == "digital":
            if download_size is None or download_size < 0:
                raise ValueError("Digital product requires a non-negative download size.")
            return DigitalProduct(product_id, name, price, stock_quantity, download_size, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
