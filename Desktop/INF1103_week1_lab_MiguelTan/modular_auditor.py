

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

def calculate_tax(amount, tax_rate):
    tax = amount * tax_rate
    return tax

def generate_report(total_units, failed_entries):
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_entries)

def main():
    inventory = 0
    failed_entries = 0 
    tax_rate = 0.1     
    exit_program = False

    while not exit_program:
        stock = get_valid_input()

        if stock == "quit":
            exit_program = True

        elif stock is None:
            failed_entries += 1
            continue

        inventory = process_delivery(inventory, stock)
        tax = calculate_tax(stock, tax_rate)

        if inventory > 500:
                    print("OVERSTOCK ALERT!")
                    break

    generate_report(inventory, failed_entries)
    
if __name__ == "__main__":
    main()

        

        
        
