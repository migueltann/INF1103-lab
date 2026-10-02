import io_manager
import ai_manager

def main():
    io_manager.display_welcome_banner()

    io_manager.display_menu()

    choice = io_manager.get_user_choice()

    if choice == "1":
        user_inputs = io_manager.collect_user_requirements()

        if user_inputs is None:
            print("Exiting the program.")
            return

        destination = user_inputs["destination"]

        try:
            recommendations = ai_manager.generate_recommendations(destination)
        except Exception as error:
            print(f"AI generation failed: {error}")
            return

        print(recommendations)
        
if __name__ == "__main__":
    main()

