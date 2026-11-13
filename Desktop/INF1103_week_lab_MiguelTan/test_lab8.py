from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


class Lab8Tests(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S001", "Tech Supplier", "tech@example.com")
        self.physical = PhysicalProduct("P001", "Laptop", 1200.0, 15, 2.5, supplier)
        self.digital = DigitalProduct("D001", "Photoshop", 99.0, 20, 500.0, supplier)

    def test_order_owns_distinct_lines_that_share_a_product(self) -> None:
        first = Order("O001")
        second = Order("O002")
        self.assertEqual(first.calculate_total(), 0.0)
        first.add_order_line(self.physical, 2)
        second.add_order_line(self.physical, 1)

        self.assertEqual(len(first.order_lines) + len(second.order_lines), 2)
        self.assertIsNot(first.order_lines[0], second.order_lines[0])
        self.assertIs(first.order_lines[0].product, second.order_lines[0].product)

        first.add_order_line(self.digital, 3)
        for line, subtotal in zip(first.order_lines, (2400.0, 297.0), strict=True):
            print(f"{line.product.get_id()} x {line.quantity}: ${line.calculate_subtotal():.2f}")
            self.assertEqual(line.calculate_subtotal(), subtotal)
        self.assertEqual(first.calculate_total(), 2697.0)

        first.remove_order_line(0)
        self.assertEqual(first.calculate_total(), 297.0)
        self.assertEqual(second.calculate_total(), 1200.0)
        self.assertIs(second.order_lines[0].product, self.physical)

    def test_order_rejects_nonpositive_quantity(self) -> None:
        order = Order("O001")
        with self.assertRaises(ValueError):
            order.add_order_line(self.physical, 0)
        self.assertEqual(order.order_lines, ())

    def test_both_subclasses_support_product_operations(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)

        output = StringIO()
        with redirect_stdout(output):
            for product in inventory.products:
                product.update_stock(7)
                self.assertEqual(product.to_dict()["stock"], 7)
                self.assertIs(inventory.find_product(product.get_id()), product)
                show_product_details(product)

        for expected in (
            "Weight: 2.5 kg",
            "This product requires physical shipping.",
            "Download Size: 500.0 MB",
            "This product is delivered digitally.",
        ):
            self.assertIn(expected, output.getvalue())
        self.assertEqual(output.getvalue().count("Stock: 7"), 2)

    def test_cli_loads_legacy_data_and_round_trips_supplier_details(self) -> None:
        app = Path(__file__).with_name("main.py").resolve()
        with TemporaryDirectory() as temporary_directory:
            data = Path(temporary_directory) / "inventory.json"
            legacy_product = self.physical.to_dict()
            del legacy_product["supplier"]
            data.write_text(json.dumps([legacy_product]), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(app)],
                input=(
                    "2\n2\nD001\nPhotoshop\n99\n20\nS001\nTech Supplier\n"
                    "tech@example.com\n500\n8\nO001\nP001\n2\nD001\n3\n\n"
                    "3\nD001\n7\n7\nP001\n6\n"
                ),
                text=True, capture_output=True, cwd=temporary_directory, timeout=10,
                check=True,
            )
            self.assertIn("P001 x 2: $2400.00", result.stdout)
            self.assertIn("Order total: $2697.00", result.stdout)
            self.assertIn("Product removed from inventory.", result.stdout)
            saved = json.loads(data.read_text(encoding="utf-8"))
            self.assertEqual([item["id"] for item in saved], ["D001"])
            self.assertEqual(saved[0]["stock"], 7)
            self.assertEqual(saved[0]["supplier"]["supplier_id"], "S001")

            result = subprocess.run(
                [sys.executable, str(app)],
                input="4\nD001\n6\n", text=True, capture_output=True,
                cwd=temporary_directory, timeout=10, check=True,
            )
            self.assertIn("Contact Email: tech@example.com", result.stdout)


if __name__ == "__main__":
    unittest.main()
