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

def process_delivery(current_total, new_value):
    current_total += new_value
    return current_total

def calculate_tax(amount):
    tax = amount * 0.1
    return tax

def generate_report(total_units, failed_entries):
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_entries)



        

        if inventory > 500:
            print("OVERSTOCK ALERT!")
            break
        
