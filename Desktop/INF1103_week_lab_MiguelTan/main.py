from product_factory import ProductFactory
from input_helpers import get_positive_float
from csv_loader import load_products
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount
from inventory import Inventory
from order import Order
from supplier import Supplier

import json
import os

inventory = Inventory()


# Save inventory to JSON file
def save_inventory() -> None:
    product_data = []

    for product in inventory.products:
        product_data.append(product.to_dict())

    with open("inventory.json", "w") as file:
        json.dump(product_data, file, indent=4)

    print("Inventory saved successfully!")


# Load inventory from JSON file


def load_inventory() -> None:
    if os.path.exists("inventory.json"):
        try:
            with open("inventory.json", "r") as file:
                product_data = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            print(f"Unable to load inventory: {error}")
            return

        for item in product_data:
            supplier_data = item.get("supplier")

            if supplier_data:
                supplier = Supplier(
                    supplier_data["supplier_id"],
                    supplier_data["name"],
                    supplier_data["contact_email"]
                )
            else:
                # Support older Lab 7 products
                supplier = Supplier(
                    "UNKNOWN",
                    "Unknown Supplier",
                    "unknown@example.com"
                )

            try:
                new_product = ProductFactory.create(
                    item.get("type", ""), item["id"], item["name"],
                    float(item["price"]), int(item["stock"]), supplier,
                    weight=item.get("weight"),
                    download_size=item.get("download_size")
                )
            except (ValueError, KeyError, TypeError) as error:
                print(f"Skipping invalid saved product: {error}")
                continue

            inventory.add_product(new_product)

        print("Inventory loaded successfully!")

    else:
        print("No saved inventory found. Starting with an empty inventory.")


# Display menu
def display_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("7. Remove Product")
    print("8. Price an Order")
    print("9. Load Products from CSV")
    print("10. Price an Order with Discount")
    print("----------------------------")


# Add a new product
def handle_add_product() -> None:
    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Enter product type (1-2): ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type!")
        return

    product_id = input("Enter product ID: ").strip()

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists!")
        return

    if not product_id:
        print("Product ID cannot be empty!")
        return

    name = input("Enter product name: ").strip()

    if not name:
        print("Product name cannot be empty!")
        return

    price = get_positive_float("Enter product price: ")
    try:
        stock = int(input("Enter product stock quantity: "))
    except ValueError:
        print("Invalid input! Please enter valid numbers.")
        return

    if stock < 0:
        print("Stock cannot be negative!")
        return


    print("Enter Supplier Information:")

    supplier_id = input("Enter supplier ID: ").strip()
    supplier_name = input("Enter supplier name: ").strip()
    supplier_email = input("Enter supplier email: ").strip()

    if not supplier_id or not supplier_name or not supplier_email:
        print("Supplier information cannot be empty!")
        return

    supplier = Supplier(supplier_id, supplier_name, supplier_email)


    if product_type == "1":
        try:
            weight = float(input("Enter product weight (kg): "))
            if weight < 0:
                print("Weight cannot be negative!")
                return
        except ValueError:
            print("Invalid weight! Please enter a valid number.")
            return
        new_product = ProductFactory.create("physical", product_id, name, price, stock, supplier, weight=weight)
    else:
        try:
            file_size = int(input("Enter file size (MB): "))
            if file_size < 0:
                print("File size cannot be negative!")
                return
        except ValueError:
            print("Invalid file size! Please enter a valid number.")
            return
        new_product = ProductFactory.create("digital", product_id, name, price, stock, supplier, download_size=file_size)

    inventory.add_product(new_product)

    print(f"Product {name} added successfully!")


# Update product stock
def handle_update_stock() -> None:
    product_id = input("Enter product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product doesn't exist!")
        return

    try:
        stock = int(input("Enter new stock quantity: "))
    except ValueError:
        print("Invalid stock quantity! Please enter a whole number.")
        return

    if stock < 0:
        print("Stock cannot be negative!")
        return

    product.update_stock(stock)
    print(f"Stock updated to {stock}.")


# Search for a product
def handle_search_product() -> None:
    product_id = input("Enter product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product doesn't exist!")
    else:
        product.display_information()
        product.supplier.display_information()


def handle_remove_product() -> None:
    product_id = input("Enter product ID: ").strip()
    if inventory.find_product(product_id) is None:
        print("Product doesn't exist!")
        return
    inventory.remove_product(product_id)
    print("Product removed from inventory.")


def handle_price_order(choose_discount: bool = False) -> None:
    order_id = input("Enter order ID: ").strip()
    if not order_id:
        print("Order ID cannot be empty!")
        return

    order = Order(order_id)
    while product_id := input("Enter product ID (blank to finish): ").strip():
        product = inventory.find_product(product_id)
        if product is None:
            print("Product doesn't exist!")
            continue
        try:
            quantity = int(input("Enter quantity: "))
            order.add_order_line(product, quantity)
        except ValueError:
            print("Quantity must be a positive whole number.")

    print(f"Order {order.order_id}")
    for line in order.order_lines:
        print(f"{line.product.get_id()} x {line.quantity}: ${line.calculate_subtotal():.2f}")
    print(f"Order total before discount: ${order.calculate_total():.2f}")
    if choose_discount:
        print("Discount: 1=None, 2=10%, 3=Bulk ($20 off $200+), 4=Student (5%)")
        choice = input("Choose discount (1-4): ").strip()
    else:
        choice = "1"
    if choice == "2":
        order.set_discount(PercentageDiscount(10))
    elif choice == "3":
        order.set_discount(BulkDiscount(200, 20))
    elif choice == "4":
        order.set_discount(StudentDiscount())
    elif choice != "1":
        print("Unknown discount; no discount applied.")
    print(f"Order total: ${order.calculate_total():.2f}")


# Main application
def main() -> None:
    load_inventory()

    while True:
        display_menu()
        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            handle_add_product()

        elif choice == "3":
            handle_update_stock()

        elif choice == "4":
            handle_search_product()

        elif choice == "5":
            save_inventory()

        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory()
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        elif choice == "7":
            handle_remove_product()

        elif choice == "8":
            handle_price_order()

        elif choice == "10":
            handle_price_order(choose_discount=True)
        elif choice == "9":
            path = input("CSV file path [products.csv]: ").strip() or "products.csv"
            supplier = Supplier("CSV", "CSV Supplier", "csv@example.com")
            load_products(path, inventory, supplier)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
