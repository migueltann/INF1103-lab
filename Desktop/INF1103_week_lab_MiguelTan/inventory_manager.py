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

add_product()
display_all()