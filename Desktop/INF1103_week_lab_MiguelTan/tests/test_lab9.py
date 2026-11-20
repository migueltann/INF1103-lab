import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from bulk_discount import BulkDiscount
from csv_loader import load_products
from digital_product import DigitalProduct
from input_helpers import get_positive_float
from inventory import Inventory
from no_discount import NoDiscount
from order import Order
from order_line import OrderLine
from percentage_discount import PercentageDiscount
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from student_discount import StudentDiscount
from supplier import Supplier


class Lab9Tests(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Supplier", "s@example.com")
        self.product = ProductFactory.create("physical", "P1", "Lamp", 25, 10, self.supplier, weight=1)

    def test_strategies_and_switching(self):
        order = Order("O1")
        order.add_order_line(self.product, 10)
        self.assertEqual(order.calculate_total(), 250)
        order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)
        order.set_discount(StudentDiscount())
        self.assertEqual(order.calculate_total(), 237.5)
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_factory_and_validation(self):
        self.assertIsInstance(self.product, PhysicalProduct)
        self.assertIsInstance(ProductFactory.create("digital", "D1", "App", 12, 3, self.supplier, download_size=50), DigitalProduct)
        with self.assertRaisesRegex(ValueError, "Unknown product type"):
            ProductFactory.create("service", "S1", "Install", 30, 2, self.supplier)
        for price, stock in [(0, 2), (-5, 2), (10, -1)]:
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "X", "Bad", price, stock, self.supplier, weight=1)
        with self.assertRaises(ValueError):
            self.product.update_stock(-1)
        for quantity in [0, -1]:
            with self.assertRaises(ValueError):
                OrderLine(self.product, quantity)

    def test_retry_input(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(get_positive_float("Price: "), 12.5)
            self.assertIn("Please enter a valid number", output.getvalue())
            self.assertIn("Please enter a number greater than zero", output.getvalue())

    def test_csv_valid_rows_and_missing_file(self):
        inventory = Inventory()
        sample = Path(__file__).resolve().parent.parent / "products.csv"
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            load_products(str(sample), inventory, self.supplier)
        self.assertEqual(len(inventory.products), 3)
        self.assertIn("Skipping row 4", output.getvalue())
        self.assertIn("Skipping row 5", output.getvalue())
        self.assertIn("3 products loaded.", output.getvalue())
        self.assertTrue(output.getvalue().rstrip().endswith("Load attempt finished."))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            load_products(str(sample) + ".missing", inventory, self.supplier)
        self.assertIn("Products file not found", output.getvalue())
        self.assertTrue(output.getvalue().rstrip().endswith("Load attempt finished."))


if __name__ == "__main__":
    unittest.main()
