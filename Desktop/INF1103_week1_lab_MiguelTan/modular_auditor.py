inventory = 0
failed_entries = 0

def get_valid_input():
    stock = input("Enter stock quantity (or 'quit' to exit): ")
    if stock.lower() == "quit":
        return "quit"

    elif not stock.isdigit():
        print("Error: Please enter a valid positive integer.")
        return None

    else:
        return int(stock)

while True:
    stock = get_valid_input()

    if stock.lower() == "quit":
        break

    elif not stock.isdigit():
        print("Error: Please enter a valid positive integer.")
        failed_entries += 1
        continue

    else:
        stock = int(stock)
        inventory += stock

        print("Current inventory:", inventory)

        if inventory > 500:
            print("OVERSTOCK ALERT!")
            break
        
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)