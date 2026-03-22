

# Import the SeatingSystem class from Booking_System 
from Booking_System import SeatingSystem


def show_menu():
    
    print("\n=======================================")
    print("     APACHE AIRLINES BOOKING SYSTEM    ")
    print("=======================================")
    print("1. Check availability of seat")
    print("2. Book a seat")
    print("3. Free a seat")
    print("4. Show booking status")
    print("5. Show number of available seats")
    print("6. Exit program")
    print("=======================================")


# function that runs the program, creates the seating grid and displays menu options
def main():

    #Creates a SeatingSystem object when the program starts
    system = SeatingSystem()

    # Welcome message for when the user first opens the program
    print("Welcome to the Apache Airlines!")

    # Keep showing the menu after every action until the user chooses to exit
    while True:

        # Show the menu options
        show_menu()

        # Ask the user to choose an option
        choice = input("Please enter your choice (1-6): ")

        # Option 1, allows the user to check seat availability
        if choice == "1":
            seat = input("Enter the seat code (e.g. 1A, 45C): ").upper()
            result = system.check_availability(seat)
            print("\n" + result)

        # Option 2, allows the user to book a seat
        elif choice == "2":
            seat = input("Enter the seat code to book (e.g. 1A, 45C): ").upper()
            result = system.book_seat(seat)
            print("\n" + result)

        # Option 3, allows the user to free a seat
        elif choice == "3":
            seat = input("Enter the seat code to free (e.g. 1A, 45C): ").upper()
            result = system.free_seat(seat)
            print("\n" + result)

        # Option 4, shows the full layout of the Burak757
        elif choice == "4":
            system.show_grid()

        # Option 5, shows the number of available seats
        elif choice == "5":
            system.count_available()

        # Option 6, allows the user to exit the program
        elif choice == "6":
            print("\nThank you for using Apache Airlines. Goodbye!")
            break  

        # If the user inputs a non existing option, print an error message
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")


# Runs the main function
main()