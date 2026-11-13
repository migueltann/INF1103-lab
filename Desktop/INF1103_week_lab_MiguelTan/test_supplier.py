from contextlib import redirect_stdout
from io import StringIO
import unittest

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from supplier import Supplier


class SupplierTests(unittest.TestCase):
    def test_products_keep_the_same_supplier(self) -> None:
        supplier = Supplier("S001", "Apple", "apple@example.com")
        phone = PhysicalProduct("P001", "iPhone", 1200.0, 10, 0.2, supplier)
        app = DigitalProduct("D001", "App", 25.5, 20, 100.0, supplier)
        self.assertIs(phone.supplier, supplier)
        self.assertIs(app.supplier, supplier)

        del supplier

        for product in (phone, app):
            output = StringIO()
            with redirect_stdout(output):
                product.supplier.display_information()
            self.assertIn("Supplier ID: S001", output.getvalue())
            self.assertIn("Contact Email: apple@example.com", output.getvalue())

        self.assertIs(phone.supplier, app.supplier)

    def test_supplier_can_exist_without_products(self) -> None:
        supplier = Supplier("S001", "Apple", "apple@example.com")
        product = PhysicalProduct("P001", "iPhone", 1200.0, 10, 0.2, supplier)
        del product
        self.assertEqual(supplier.to_dict()["name"], "Apple")


if __name__ == "__main__":
    unittest.main()
