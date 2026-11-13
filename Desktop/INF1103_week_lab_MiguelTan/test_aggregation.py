import unittest

from inventory import Inventory
from physical_product import PhysicalProduct
from supplier import Supplier


class AggregationTests(unittest.TestCase):
    def test_transfer_keeps_same_product(self) -> None:
        supplier = Supplier("S001", "Apple", "apple@example.com")
        product = PhysicalProduct("P001", "iPhone", 1200.0, 10, 0.2, supplier)
        inventory_a = Inventory()
        inventory_b = Inventory()

        inventory_a.add_product(product)
        self.assertIs(inventory_a.find_product("P001"), product)
        inventory_a.remove_product("P001")

        self.assertIsNone(inventory_a.find_product("P001"))
        self.assertEqual(inventory_a.products, [])
        self.assertEqual(product.get_id(), "P001")
        self.assertEqual(product.calculate_shipping_cost(), 1.0)

        inventory_b.add_product(product)
        self.assertIs(inventory_b.search_product("P001"), product)
        inventory_b.remove_product("MISSING")
        self.assertIs(inventory_b.find_product("P001"), product)


if __name__ == "__main__":
    unittest.main()
