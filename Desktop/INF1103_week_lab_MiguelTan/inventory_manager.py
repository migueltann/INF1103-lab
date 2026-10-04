import json
import os

inventory = [
    {
        "id": "P001",
        "name": "Laptop",
        "price": 1200.00,
        "stock": 15
    },
    {
        "id": "P002",
        "name": "Mouse",
        "price": 25.50,
        "stock": 40
    },
    {
        "id": "P003",
        "name": "Keyboard",
        "price": 45.00,
        "stock": 25
    }
]

def save_inventory():
    with open("inventory.json", "w") as file:
        json.dump(inventory, file)
        print("Inventory saved to inventory.json.")

def load_inventory():
    global inventory
    if os.path.exists("inventory.json"):
        with open("inventory.json", "r") as file:
            inventory = json.load(file)
    else:
        inventory = []
        

def display_all():
    print("Current Inventory:")
    for item in inventory:
        print(f"ID: {item['id']}, Name: {item['name']}, Price: ${item['price']:.2f}, Stock: {item['stock']}")

def add_product():
    product_id = input("Enter product ID: ")
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    stock = int(input("Enter product stock quantity: "))
    
    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    
    inventory.append(new_product)
    print(f"Product {name} added successfully.")

def update_stock():
    product_id = input("Enter product ID: ")

    for item in inventory:
        if item['id'] == product_id:
            new_stock_value = int(input("Enter new product stock quantity: "))
            item['stock'] = new_stock_value
            print(f"Stock for product {item['name']} updated to {new_stock_value}.")
            return

    print("Product not found.")

def search_product():
    product_id = input("Enter product ID: ")

    for item in inventory:
        if item['id'] == product_id:
            print(item)
            return

    print("Product not found")


load_inventory()
display_all()