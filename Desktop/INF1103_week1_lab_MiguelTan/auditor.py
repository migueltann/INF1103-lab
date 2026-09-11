inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or 'quit' to exit): ")

    if stock.lower() == "quit":
        break

    elif not stock.isdigit():
        print("Error: Please enter a valid positive integer.")
        failed_entries += 1
        continue