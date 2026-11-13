import unittest

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from supplier import Supplier


class ShippingTests(unittest.TestCase):
    def test_shipping_is_a_physical_product_capability(self) -> None:
        supplier = Supplier("S001", "Tech Supplier", "tech@example.com")
        physical = PhysicalProduct("P001", "Laptop", 1200.0, 15, 2.5, supplier)
        digital = DigitalProduct("D001", "Photoshop", 99.0, 20, 500.0, supplier)

        self.assertIsInstance(physical, CanBeShipped)
        self.assertEqual(physical.calculate_shipping_cost(), 12.5)
        self.assertNotIsInstance(digital, CanBeShipped)


if __name__ == "__main__":
    unittest.main()
