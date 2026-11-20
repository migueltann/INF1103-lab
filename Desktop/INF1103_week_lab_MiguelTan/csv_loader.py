import csv
from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.DictReader(file)
            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type = row["product_type"].strip()
                    product = ProductFactory.create(
                        product_type, row["product_id"], row["name"],
                        float(row["price"]), int(row["stock_quantity"]), supplier,
                        weight=1.0 if product_type == "physical" else None,
                        download_size=0.0 if product_type == "digital" else None,
                    )
                    inventory.add_product(product)
                    loaded += 1
                except (ValueError, TypeError, KeyError) as error:
                    print(f"Skipping row {row_number}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
