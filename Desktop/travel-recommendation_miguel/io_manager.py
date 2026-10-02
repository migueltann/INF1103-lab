EXIT_COMMANDS = {"exit", "quit", "q"}

def display_welcome_banner():
    print("========================================")
    print("       TRAVEL RECOMMENDATION SYSTEM")
    print("========================================")

def display_menu():
    print("\n1. Generate Travel Recommendations")
    print("2. View Saved Recommendations")
    print("3. Exit")


def get_user_choice():
    while True:
        choice = input("Enter your choice (1-3): ").strip()

        if choice in {"1", "2", "3"}: #take note
            return choice
        else:
            print("Please enter 1, 2, or 3.")

def is_exit(value):
    return value.strip().lower() in EXIT_COMMANDS

def get_required_text(prompt):
    while True:
        value = input(prompt).strip()

        if is_exit(value):
            return None

        if value: #need use pi country extension
            return value

        print("This field is required.")

def get_optional_text(prompt):
    value = input(prompt).strip()

    if is_exit(value):
        return None

    return value

def get_positive_float(prompt):
    while True:
        value = input(prompt).strip()

        if is_exit(value):
            return None

        try: 
            number = float(value)

            if number > 0:
                return number
            else:
                print("Please enter a number greater than 0")

        except ValueError:
            print("Please enter a valid number. ")

def get_choice(prompt, choices, default=None):
    while True:
        print(prompt)

        for i in range(len(choices)):
            print(f"{i + 1}. {choices[i]}")

        user_input = input("Enter your choice: ").strip()

        if is_exit(user_input):
            return None

        if not user_input and default is not None:
            return default

        try:
            choice_number = int(user_input)

            if 1 <= choice_number <= len(choices):
                return choices[choice_number - 1]
            else:
                print("Please select one of the available options.")

        except ValueError:
            print("Please enter a valid number.")

def _split_csv(value):
    items = value.split(",")

    cleaned_items = []

    for item in items:
        clean_item = item.strip()
        if clean_item:
            cleaned_items.append(clean_item)

    return cleaned_items

def collect_user_requirements():
    print("\n--- Travel Requirements ---")
    print("Type 'exit', 'quit', or 'q' at any time to cancel.\n")

    destination = get_required_text("Enter your destination: ")

    if destination is None:
        return None

    max_activity_spend = get_positive_float("Maximum spend per activity per person (SGD): ")

    if max_activity_spend is None:
        return None

    max_meal_spend = get_positive_float("Maximum spend per meal per person (SGD): ")

    if max_meal_spend is None:
        return None

    interests_input = get_required_text("Enter your interests (separated by commas): ") #might need to add Any option

    if interests_input is None:
        return None

    interests = _split_csv(interests_input)

    preferred_activities_input = get_required_text("Enter your preferred activities (separated by commas): ") #might need to add Any option

    if preferred_activities_input is None:
        return None

    preferred_activities = _split_csv(preferred_activities_input)

    must_visit_input = get_optional_text("Enter must-visit spots (separated by commas, or press Enter to skip): ")

    if must_visit_input is None:
        return None

    must_visit_spots = _split_csv(must_visit_input)

    activities_to_avoid_input = get_optional_text("Enter activities or locations to avoid (separated by commas, or press Enter to skip): ")

    if activities_to_avoid_input is None:
        return None

    activities_to_avoid = _split_csv(activities_to_avoid_input)

    transport = get_choice("Preferred transport [Any] (Walk/Transit/Taxi/Any): ", ["Walk", "Transit", "Taxi", "Any"], "Any",) #might need to remove

    if transport is None:
        return None

    dietary_input = get_optional_text("Enter dietary requirements (separated by commas, or press Enter to skip): ") #becomes a list, rather than 1 option

    if dietary_input is None:
        return None

    dietary_requirements = _split_csv(dietary_input)

    user_requirements = {
        "destination": destination,
        "max_activity_spend": max_activity_spend,
        "max_meal_spend": max_meal_spend,
        "interests": interests,
        "preferred_activities": preferred_activities,
        "must_visit": must_visit_spots,
        "avoid_list": activities_to_avoid,
        "preferred_transport": transport,
        "dietary_requirements": dietary_requirements
}

    return user_requirements

def display_input_summary(data):
    print("\n--- Your Travel Requirements ---")

    print(f"Destination: {data['destination']}")
    print(f"Maximum spend per activity: SGD {data['max_activity_spend']:.2f}")
    print(f"Maximum spend per meal: SGD {data['max_meal_spend']:.2f}")
    print(f"Interests: {', '.join(data['interests'])}")
    print(f"Preferred activities: {', '.join(data['preferred_activities'])}")
    print(f"Must-visit spots: {', '.join(data['must_visit']) or 'None'}")
    print(f"Avoid list: {', '.join(data['avoid_list']) or 'None'}")
    print(f"Dietary requirements: {', '.join(data['dietary_requirements']) or 'None'}")
    print(f"Preferred transport: {data['preferred_transport']}")


#========================================================================================================================
#can commit above first then move on to ai_manager