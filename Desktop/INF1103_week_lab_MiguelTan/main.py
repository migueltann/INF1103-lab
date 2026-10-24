from product import Product
from inventory import Inventory

import json
import os

inventory = Inventory()


# Save inventory to JSON file
def save_inventory():
    product_data = []

    for product in inventory.products:
        product_data.append(product.to_dict())

    with open("inventory.json", "w") as file:
        json.dump(product_data, file, indent=4)

    print("Inventory saved successfully!")


# Load inventory from JSON file
def load_inventory():
    if os.path.exists("inventory.json"):
        with open("inventory.json", "r") as file:
            product_data = json.load(file)

        for item in product_data:
            new_product = Product(
                item["id"],
                item["name"],
                item["price"],
                item["stock"]
            )
            inventory.add_product(new_product)

        print("Inventory loaded successfully!")

    else:
        print("No saved inventory found. Starting with an empty inventory.")


# Display menu
def display_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# Add a new product
def handle_add_product():
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

    try:
        price = float(input("Enter product price: "))
        stock = int(input("Enter product stock quantity: "))
    except ValueError:
        print("Invalid input! Please enter valid numbers.")
        return

    if price < 0 or stock < 0:
        print("Price and stock cannot be negative!")
        return

    new_product = Product(product_id, name, price, stock)

    inventory.add_product(new_product)

    print(f"Product {name} added successfully!")


# Update product stock
def handle_update_stock():
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
def handle_search_product():
    product_id = input("Enter product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product doesn't exist!")
    else:
        product.display_information()


# Main application
def main():
    load_inventory()

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

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

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()